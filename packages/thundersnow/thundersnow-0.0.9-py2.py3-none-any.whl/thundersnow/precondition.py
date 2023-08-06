"""
Validate preconditions, state, and other invariants in a generic
way that is semantically explicitly and raises common exceptions.
"""
import logging

from thundersnow.predicate import is_not_empty

__all__ = (
    'PreconditionError',
    'IllegalArgumentError',
    'IllegalStateError',
    'check_argument',
    'check_state'
)


LOG = logging.getLogger(__name__)


class PreconditionError(Exception):
    pass


class IllegalArgumentError(PreconditionError):
    pass


class IllegalStateError(PreconditionError):
    pass


def check_argument(expr, *errormsg, **kwargs):
    # type: (bool, *str, **Exception) -> bool
    """Throw an IllegalArgumentError if the expression is False::

         MAX_NAME_LEN = 25

         def change_name(name):
            check_argument(len(name) <= MAX_NAME_LEN, 'name exceeds max length')
            # etc.

    """
    Error = kwargs.get('Error', IllegalArgumentError)
    if expr is False:
        message = _format_error_message(errormsg, 'Argument precondition was not met')
        raise Error(message)
    return expr


def check_state(expr, *errormsg, **kwargs):
    # type: (bool, *str, **Exception) -> bool
    """Throw an IllegalStateException if the expression is False. Take the
    following class method which uses the instances store file
    descriptor to write an update to a file:

         def write_update(self):
            check_state(not self.fd.closed(), 'Cannot write to file, file is closed')
            # etc.

    Should be used to indicate semantically different precondition
    violations than :func:`check_argument`. State preconditions should
    be validating state external to the method or function.
    """
    Error = kwargs.get('Error', IllegalStateError)
    if expr is False:
        message = _format_error_message(errormsg, 'State precondition was not met')
        raise Error(message)
    return expr


def _format_error_message(errormsg, default):
    if is_not_empty(errormsg):
        try:
            return errormsg[0].format(*errormsg[1:])
        except Exception:
            LOG.exception('Error formatting error message {}'.format(errormsg))
    return default
