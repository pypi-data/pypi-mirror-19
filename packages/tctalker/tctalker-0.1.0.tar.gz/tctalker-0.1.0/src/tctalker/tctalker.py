"""
tctalker.py
~~~~~~~~~~~~~~~~~
usage: tctalker.py [-h]
                   [--conf json-config-file]
                   [--verbose]
                   {status,cancel,rerun,report_completed|resolve} $taskId1 $taskId2

config-file must be a JSON object following this structure:
{
    "credentials": {
        "clientId": "...",
        "accessToken": "...",
    }
}

This script is to be used to perform various operations against Taskcluster API
(e.g. rerun, cancel, resolve)
"""

import json
import logging
import argparse
import asyncio
from taskcluster.async import Queue, Scheduler

log = logging.getLogger(__name__)


class TCTalker(object):
    """The base TCTalker class"""

    def __init__(self, options):
        cert = options["credentials"].get("certificate")
        if cert:
            options["credentials"]["certificate"] = json.dumps(cert)
        self.queue = Queue(options)
        self.scheduler = Scheduler(options)
        log.debug("Dict of options: %s", options)

    async def _get_last_run_id(self, task_id):
        """Private quick method to retrieve the last run_id for a job"""
        curr_status = await self.queue.status(task_id)
        log.debug("Current job status: %s", curr_status)
        return curr_status['status']['runs'][-1]['runId']

    async def _claim_task(self, task_id):
        """Method to call whenever a task operation needs claiming first"""
        curr_status = await self.queue.status(task_id)
        run_id = curr_status['status']['runs'][-1]['runId']
        log.debug("Current job status: %s", curr_status)
        log.debug("Run id is %s", run_id)
        payload = {
            "workerGroup": curr_status['status']['workerType'],
            "workerId": "TCTalker",
        }
        await self.queue.claimTask(task_id, run_id, payload)
        return run_id

    async def status(self, task_id):
        """Map over http://docs.taskcluster.net/queue/api-docs/#status"""
        return await self.queue.status(task_id)

    async def cancel(self, task_id):
        """Map over http://docs.taskcluster.net/queue/api-docs/#cancelTask"""
        log.info("Cancelling %s...", task_id)
        res = await self.queue.cancelTask(task_id)
        log.info("Cancelled %s", task_id)
        return res

    async def rerun(self, task_id):
        """Map over http://docs.taskcluster.net/queue/api-docs/#rerunTask"""
        log.info("Rerunning %s...", task_id)
        return await self.queue.rerunTask(task_id)

    async def report_completed(self, task_id):
        """Map http://docs.taskcluster.net/queue/api-docs/#reportCompleted"""
        log.info("Resolving %s...", task_id)
        await self._claim_task(task_id)
        run_id = await self._get_last_run_id(task_id)
        return await self.queue.reportCompleted(task_id, run_id)

    async def cancel_graph(self, task_graph_id):
        """ Walk the graph and cancel all pending/running tasks """
        graph = await self.scheduler.inspect(task_graph_id)
        log.debug("Current graph information %s", graph)
        tasks = graph.get('tasks', [])
        return await asyncio.wait([self.cancel(t["taskId"]) for t in tasks])

    resolve = report_completed

async def async_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["cancel", "rerun", "status",
                                           "report_completed", "resolve",
                                           "cancel_graph"],
                        help="action to be performed")
    parser.add_argument("taskIds", metavar="$taskId1 $taskId2 ....",
                        nargs="+", help="task ids to be processed")
    parser.add_argument("--conf", metavar="json-conf-file", dest="config_file",
                        help="Config file containing login information for TC",
                        required=True, type=argparse.FileType('r'))
    parser.add_argument("-v", "--verbose", action="store_const",
                        dest="loglevel", const=logging.DEBUG,
                        default=logging.INFO,
                        help="Increase output verbosity")
    args = parser.parse_args()

    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                        level=args.loglevel)

    action, task_ids = args.action, args.taskIds
    taskcluster_config = None
    if args.config_file:
        log.info("Attempt to read configs from json config file...")
        taskcluster_config = json.load(args.config_file)

    log.info("Wrapping up a TCTalker object to apply <%s> action", action)
    tct = TCTalker(taskcluster_config)
    func = getattr(tct, action)
    for _id in task_ids:
        log.info("Run %s action for %s taskId...", action, _id)
        ret = await func(_id)
        log.debug("Status returned for %s: %s", _id, ret)


def main():
    asyncio.get_event_loop().run_until_complete(async_main())

if __name__ == "__main__":
    main()
