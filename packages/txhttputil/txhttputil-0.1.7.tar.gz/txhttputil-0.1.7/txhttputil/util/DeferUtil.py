"""
 * Created by Synerty Pty Ltd
 *
 * This software is open source, the MIT license applies.
 *
 * Website : http://www.synerty.com
 * Support : support@synerty.com
"""

import logging

from twisted.internet.defer import maybeDeferred
from twisted.internet.threads import deferToThread

logger = logging.getLogger()

__author__ = 'synerty'


def printFailure(failure):
    logger.error(failure)
    return failure


def deferToThreadWrap(funcToWrap):
    def func(*args, **kwargs):
        d = deferToThread(funcToWrap, *args, **kwargs)
        d.addErrback(printFailure)
        return d

    return func


def maybeDeferredWrap(funcToWrap):
    """ Maybe Deferred Wrap

    A decorator that ensures a function will return a deferred.

    """
    def func(*args, **kwargs):
        return maybeDeferred(funcToWrap, *args, **kwargs)
    return func