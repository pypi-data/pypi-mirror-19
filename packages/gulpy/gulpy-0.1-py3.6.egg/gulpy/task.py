"""Module responsible to control the tasks."""
import sys

from datetime import datetime
from multiprocessing import freeze_support
from multiprocessing import Pool

from gulpy.log import fail, log, ok, set_start_time
from gulpy.stream import Stream

tasks = {}
start_time = datetime.now()


class Task(object):
    """Decorator to register tasks.

    :note:
        To determine if task fail, just return False

    >>> @Task('TaskName')
    ... def task():
    ...     do_something()

    """

    def __init__(self, task_name: str, silent: bool=False) -> None:
        """Constructor.

        :param task_name: Task name
        :param silent: Disables log output
        """
        self.task_name = task_name
        self.silent = silent

    def __call__(self, func):
        """Decorator call."""
        tasks[self.task_name] = (func, self.silent)
        return func


def _nostdout(func: object) -> object:
    """Disable STDOUT for run_task.

    TODO use contextlib.redirec_stdout

    """
    save_stdout = sys.stdout

    def stdout_off():
        sys.stdout = None
        return func()
    func = stdout_off()
    sys.stdout = save_stdout
    return func


def _run(task: str, start: datetime) -> None:
    """"Run the task by its name.

    :param task: str:
    :param start: datetime:

    """
    set_start_time(start)

    if tasks[task][1]:
        log(task, 'Started - Silent Mode')
        task_result = _nostdout(tasks[task][0])
    else:
        log(task, 'Started')
        task_result = tasks[task][0]()

    if type(task_result) is Stream:
        task_result.set_task(task)
        task_result = task_result.execute()

    if task_result or task_result is None:
        ok(task, 'Finished')
        return

    fail(task, 'Failed')
    sys.exit(1)


def _run_async(task_list: list) -> None:
    """Run a list of task by its names.

    :param task_list: list:

    """
    pool = Pool(processes=len(task_list))

    results = [pool.apply_async(_run, (task, start_time,))
               for task in task_list]

    for task in results:
        task.get()


def run_task(*tasks_to_execute: [str, list]) -> None:
    """Programmatically runs tasks, sequentially or parallel.

    :param tasks_to_execute: A collection of strings and lists of tasks to
        execute

    >>> run_task('Task1', 'Task2') # Will run 'Task1' and after 'Task2'
    >>> run_task('Task1', ['Task2', 'Task3'], 'Task4') # Will run 'Task1'
    ... #    and after 'Task2' and 'Task3' in parallel and after 'Task4'

    """
    global start_time
    start_time = datetime.now()

    for i, task in enumerate(tasks_to_execute):
        if type(task) is str:
            _run(task, start_time)
        elif type(task) is list:
            _run_async(task)

if __name__ == 'task':
    freeze_support()
