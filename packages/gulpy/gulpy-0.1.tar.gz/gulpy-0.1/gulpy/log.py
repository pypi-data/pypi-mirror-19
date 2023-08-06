"""Module responsible to print formatted outputs.

>>> from gulpy import log
>>> log('TaskName', 'LOG')
[0:00:00](TaskName): LOG

"""
import ctypes
import os

from datetime import datetime
from multiprocessing import freeze_support

# If windows, enable ANSI characters
if os.name == 'nt':
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

start_time = datetime.now()

colors = {
    'green': '\033[92m',
    'yellow': '\033[93m',
    'cyan': '\033[96m',
    'blue': '\033[36m',
    'red': '\033[91m',
    'reset': '\033[0m'
}


def set_start_time(start: datetime) -> None:
    """Define the time that the script started the execution.

    :param start: Datetime that the task execution started

    """
    global start_time
    start_time = start


def log(task_name: str, message: str) -> None:
    """Log message in standard color.

    :param task_name: Name of the task to be printed
    :param message: The message itself

    """
    _print_message(task_name, message)


def ok(task_name: str, message: str) -> None:
    """Log message in green color.

    :param task_name: Name of the task to be printed
    :param message: The message itself

    """
    _print_message(task_name, message, 'Ok')


def warn(task_name: str, message: str) -> None:
    """Log message in yellow color.

    :param task_name: Name of the task to be printed
    :param message: The message itself

    """
    _print_message(task_name, message, 'Warning')


def fail(task_name: str, message: str) -> None:
    """Log message in red color.

    :param task_name: Name of the task to be printed
    :param message: The message itself

    """
    _print_message(task_name, message, 'Fail')


def _print_message(task_name: str, message: str, message_type: str='') -> None:
    """Print the received message formatted.

    :param task_name: str:
    :param message: str:
    :param message_type: str:  (Default value = '')

    """
    now_time = datetime.now() - start_time
    formatted_time = str(now_time).split('.')[0]

    output = '[{}{}{}]'.format(colors['cyan'],
                               formatted_time,
                               colors['reset'])

    output += '({}{}{}): '.format(colors['blue'],
                                  task_name,
                                  colors['reset'])

    if message_type == 'Ok':
        output += colors['green']
    elif message_type == 'Warning':
        output += colors['yellow']
    elif message_type == 'Fail':
        output += colors['red']

    output += message + colors['reset']

    print(output)

if __name__ == 'log':
    freeze_support()
