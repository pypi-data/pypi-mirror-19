
class ThreadingFuturesError(Exception):
    """
    Base exception
    """


class NotCallableError(ThreadingFuturesError):
    """
    Raised when fn argument passed in Future constructor
    is not callable
    """


class CancelledError(ThreadingFuturesError):
    """
    Cancelled error
    """


class AlreadyRunError(ThreadingFuturesError):
    """
    Raised when done callback is trying to be set when future is already run
    """
