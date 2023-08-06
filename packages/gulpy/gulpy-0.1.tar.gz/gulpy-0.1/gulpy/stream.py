"""Module responsible to control file streams."""

from io import StringIO
from os import getcwd, makedirs
from os.path import abspath, join, isdir
from sys import exit as _exit

from .log import warn, fail


class Stream(object):
    r"""Class that controls the entire stream.

    >>> @Task('t1')
    ... def t1():
    ... s = Stream().src('file')\
    ...             .pipe(fun1)\
    ...             .dest('./dist')
    ... return s

    """

    def __init__(self, stop_on_error: bool=True) -> None:
        """Constructor of Stream.

        :param stop_on_error: Stop the execution in case of error

        """
        self.stop_on_error = stop_on_error
        self.files = []
        self.dest_path = None
        self.pipes = []
        self.task_name = ''
        self.read = True

    def set_task(self, task_name: str) -> None:
        """Set the Task Name to be used in the logs.

        :note:
            Internal use only

        :param task_name: Task name

        """
        self.task_name = task_name

    def src(self, files: [str, list], read: bool=True) -> object:
        """Define the files that will be readed.

        :param files: Files to be streamed
        :param read: Determine if will read the file contents
        :returns: The `Stream` instance

        >>> Stream().src('file')
        >>> Stream().src(['file', 'file2'])

        """
        self.read = read

        if type(files) is str:
            files = [files]
        self.files = files

        return self

    def pipe(self, func: object) -> object:
        r"""Define a function or class instance to receive the files.

        :note:
            `Class`: Needs to have a `run` method with the following
                signature ``def run(self, files):``
            `Function`: Needs to have the following signature
                ``def my_pipe(files):``

        :param func: ``Function`` or ``class`` that will receive files
        :returns: The ``Stream`` instance

        Pipe ``functions`` needs to be only the name of function

        >>> Stream().src('file').pipe(fun1)

        Pipe ``classes`` needs to be an instance

        >>> Stream().src('file')\
        ...         .pipe(fun1)\
        ...         .pipe(pipe_class())\
        ...         .pipe(func2)

        """
        self.pipes.append(func)
        return self

    def dest(self, path: str) -> None:
        """Set the output relative folder path.

        :param path (str): Output folder to the stream

        Examples:

        >>> Stream().src('file').pipe(fun1).dest('./dist')

        """
        self.dest_path = abspath(path)

    def execute(self) -> None:
        r"""Programmatically runs the stream.

        >>> Stream().src('file')\
        ...         .pipe(fun1)\
        ...         .dest('./dist')\
        ...         .execute()

        """
        self._treat_files()
        self._run_pipes()
        self._write_files()

    # ------------------------- METHOD OVERRIDE -------------------------------
    def __lshift__(self, items: (list, str, object)) -> object:
        """Append files or pipes to the stream.

        >>> Stream() << 'file1' # Will have file1 in files list
        >>> Stream() << func # Will have func in pipes list
        >>> Stream() << Concat('c.txt') # Will have Concat in pipes list

        """
        if type(items) is list:
            [self._treat_entry(item) for item in items]
        else:
            self._treat_entry(items)

        return self

    def __rshift__(self, dest_path: str) -> None:
        """Define the destination directory."""
        self.dest_path = dest_path

    def _treat_entry(self, item: (str, object)) -> None:
        """Treat __lshift__ entry.

        If `str`: is a file
        If `function` or `class instance`: is a pipe

        """
        if type(item) is str:
            self.files.append(item)
        else:
            self.pipes.append(item)

    # ------------------------- PRIVATE METHODS -------------------------------

    def _treat_files(self) -> None:
        """Treat the files list to be a list of dict `{'name', 'iterator'}`."""
        self.files = [{'name': file, 'iterator': self._get_file_iterator(file)}
                      for file in self.files]

    def _run_pipes(self) -> None:
        """Run the pipes, reseting the iterator pointer to start point."""
        for pipe in self.pipes:
            self._seek_files()
            self._get_pipe_result(pipe)

    def _write_files(self) -> None:
        """Write the result of each file, if dest_path was defined."""
        if not self.dest_path:
            return

        dir_path = abspath(self.dest_path)
        if not isdir(dir_path):
            makedirs(dir_path)

        for file in self.files:
            path = join(dir_path, file['name'])
            content = ''.join(file['iterator'])
            open(path, 'w+').write(content)

    def _get_file_iterator(self, file: str) -> iter:
        """Get the file iterator.

        :param file: str:
        :returns: The file iterator

        """
        result = StringIO()

        if not self.read:
            return result

        path = join(getcwd(), file)
        try:
            result = open(path, 'r')
        except FileNotFoundError:
            message = 'File not found: {}'.format(file)
            self._treat_error(message)

        return result

    def _seek_files(self) -> None:
        """Reset file iterator pointer to the start point."""
        [file['iterator'].seek(0) for file in self.files]

    def _get_pipe_result(self, pipe: object) -> None:
        """Run the pipe and get result, setting the result in self.files."""
        if callable(pipe):
            func_name = pipe.__name__
            result = pipe(self.files)
        else:
            func_name = pipe.__class__.__name__
            result = pipe.run(self.files)

        if result is False:
            message = 'Pipe execution failed: {}'.format(func_name)
            self._treat_error(message)

        if type(result) is list:
            self.files = result

    def _treat_error(self, message: str) -> None:
        """Treat message received, determining if is a wrning or error."""
        if self.stop_on_error:
            fail(self.task_name, message)
            _exit(1)
        else:
            warn(self.task_name, message)
