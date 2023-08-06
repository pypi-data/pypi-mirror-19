#!/usr/bin/env python3

import argparse
import os
import threading
import random
import time
import signal
import socket
import traceback
import multiprocessing

import redis
from redis.exceptions import ConnectionError, RedisError

import cmdserver
from dwq import Job, Disque

from gitjobdir import GitJobDir

def sigterm_handler(signal, stack_frame):
    raise SystemExit()

def parse_args():
    parser = argparse.ArgumentParser(prog='dwqw', description='dwq: disque-based work queue (worker)')

    parser.add_argument('--version', action='version', version='%(prog)s 0.1')

    parser.add_argument('-q', '--queues', type=str,
            help='queues to wait for jobs (default: \"default\")', nargs='*', default=["default"])
    parser.add_argument('-j', "--jobs",
            help='number of workers to start', type=int, default=multiprocessing.cpu_count())
    parser.add_argument('-n', '--name', type=str,
            help='name of this worker (default: hostname)', default=socket.gethostname())
    parser.add_argument('-v', "--verbose", help='enable status output', action="store_true" )

    return parser.parse_args()

shutdown = False

def worker(n, cmd_server_pool, gitjobdir, args, working_set):
    global shutdown
    print("worker %2i: started" % n)
    buildnum = 0
    while not shutdown:
        try:
            if not Disque.connected():
                time.sleep(1)
                continue
            while not shutdown:
                jobs = Job.get(args.queues)
                for job in jobs:
                    if shutdown:
                        job.nack()
                        continue
                    buildnum += 1
                    working_set.add(job.job_id)
                    before = time.time()
                    print("worker %2i: got job %s from queue %s" % (n, job.job_id, job.queue_name))

                    try:
                        repo = job.body["repo"]
                        commit = job.body["commit"]
                        command = job.body["command"]
                    except KeyError:
                        print("worker %2i: invalid job json body" % n)
                        job.done({ "status" : "error", "output" : "worker.py: invalid job description" })
                        continue

                    print("worker %2i: command=\"%s\"" % (n, command))

                    exclusive = None
                    try:
                        options = job.body.get("options") or {}
                        if options.get("jobdir") or "" == "exclusive":
                            exclusive = str(random.random())
                    except KeyError:
                        pass

                    _env = os.environ.copy()
                    _env.update({ "DWQ_REPO" : repo, "DWQ_COMMIT" : commit, "DWQ_QUEUE" : job.queue_name,
                                  "DWQ_WORKER" : args.name, "DWQ_WORKER_BUILDNUM" : str(buildnum) })
                    try:
                        _env.update(job.body["env"])
                    except KeyError:
                        pass

                    workdir = gitjobdir.get(repo, commit, exclusive=exclusive or str(n))
                    if not workdir:
                        if job.nacks < (options.get("max_retries") or 2):
                            job.nack()
                            print("worker %2i: error getting job dir, requeueing job" % n)
                        else:
                            job.done({ "status" : "error", "output" : "dwqw: error getting jobdir\n",
                                        "worker" : args.name, "runtime" : 0, "body" : job.body })
                            print("worker %2i: cannot get job dir, erroring job" % n)
                        working_set.discard(job.job_id)
                        continue

                    handle = cmd_server_pool.runcmd(command, cwd=workdir, shell=True, env=_env)
                    output, result = handle.wait(timeout=300)
                    if handle.timeout:
                        result = "timeout"

                    if (result not in { 0, "0", "pass" }) and job.nacks < (options.get("max_retries") or 2):
                        print("worker %2i: command:" % n, command,
                                "result:", result, "nacks:", job.nacks, "re-queueing.")
                        job.nack()
                    else:
                        runtime = time.time() - before
                        job.done({ "status" : result, "output" : output, "worker" : args.name, "runtime" : runtime, "body" : job.body })
                        print("worker %2i: command:" % n, command,
                                "result:", result, "runtime: %.1fs" % runtime)
                        working_set.discard(job.job_id)
                    gitjobdir.release(workdir)

        except Exception as e:
            print("worker %2i: uncaught exception" % n)
            traceback.print_exc()
            time.sleep(10)
            print("worker %2i: restarting worker" % n)


class SyncSet(object):
    def __init__(s):
        s.set = set()
        s.lock = threading.Lock()

    def add(s, obj):
        with s.lock:
            s.set.add(obj)

    def discard(s, obj):
        with s.lock:
            s.set.discard(obj)

    def empty(s):
        with s.lock:
            oldset = s.set
            s.set = set()
            return oldset

def main():
    global shutdown

    args = parse_args()

    cmd_server_pool = cmdserver.CmdServerPool(args.jobs)

    signal.signal(signal.SIGTERM, sigterm_handler)

    _dir = "/tmp/dwq.%s" % str(random.random())
    gitjobdir = GitJobDir(_dir, args.jobs)

    servers = ["localhost:7711"]
    try:
        Disque.connect(servers)
        print("dwqw: connected.")
    except:
        pass

    working_set = SyncSet()

    for n in range(1, args.jobs + 1):
        threading.Thread(target=worker, args=(n, cmd_server_pool, gitjobdir, args, working_set), daemon=True).start()

    try:
        while True:
            if not Disque.connected():
                try:
                    print("dwqw: connecting...")
                    Disque.connect(servers)
                    print("dwqw: connected.")
                except RedisError:
                    pass
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("dwqw: signal caught, shutting down")
        shutdown = True
        cmd_server_pool.destroy()
        print("dwqw: nack'ing jobs")
        jobs = working_set.empty()
        d = Disque.get()
        d.nack_job(*jobs)
        print("dwqw: cleaning up job directories")
        gitjobdir.cleanup()

