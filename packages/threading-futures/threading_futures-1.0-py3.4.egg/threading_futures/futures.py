
from threading import Event, Thread

from threading_futures.errors import (
    AlreadyRunError,
    CancelledError,
    NotCallableError,
)


class Future(Thread):
    """
    Future base class
    """

    def __init__(self, fn, *args, **kwargs):
        super(Future, self).__init__()
        self._stop = Event()
        self._run = False
        self._is_done = False
        if not callable(fn):
            raise NotCallableError("fn argument is not callable")
        self._fn = fn
        self._args = args
        self._kwargs = kwargs
        self._exception = None
        self._result = None
        self._done_callback = None

    def run(self):
        """
        Run the Future.
        """
        self._run = True
        try:
            self._result = self._fn(*self._args, **self._kwargs)
        except Exception as exc:
            self._exception = exc
        self._is_done = True
        self._run = False
        if self._done_callback:
            self._done_callback(self)

    def cancel(self):
        """
        Cancel future.
        If it's currently run and cannot be canceled if returns False.
        Otherwise the future will be canceled and method will return True.
        """
        if self._run:
            return False
        self._stop.set()
        return True

    def cancelled(self):
        """
        Return True if Future was cancelled.
        """
        return self._stop.is_set()

    def running(self):
        """
        Return True if Future is currently being executed and cannot be cancelled.
        """
        return self._run

    def done(self):
        """
        Return True if Future was cancelled or is finished.
        """
        return self._is_done or self.cancelled()

    def result(self):
        """
        Return the result of the call.
        It it was cancelled it raised CancelledError.
        If function raised any exception it will be raised by this method.
        """
        if self.cancelled():
            raise CancelledError("Cancelled future")
        if self._exception:
            raise self._exception
        return self._result

    def exception(self):
        """
        Return the exception raised by the call.
        If none exception was raised it returns None.
        """
        return self._exception

    def add_done_callback(self, func):
        """
        Attach the callable func which will be called if the future was cancelled
        or it finishes it's run.
        The only argument should be func.
        """
        if self._run or self.done():
            raise AlreadyRunError("Future is already run")
        self._done_callback = func
