"""
Helper methods for Python's logging library.
"""
import logging
from logging.handlers import TimedRotatingFileHandler
import sys


def timed_rotating_log(path, when="D", interval=1, backupCount=5):
    logger = logging.getLogger("Rotating Log")

    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler(
        path, when=when, interval=interval, backupCount=backupCount
    )

    logger.addHandler(handler)

    return logger


"""
Support for Redirector, below.
From: https://stackoverflow.com/questions/11124093/redirect-python-print-output-to-logger/11124247
"""
class _StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO, orig_stream=None):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''
        self.orig_stream = orig_stream

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
        if self.orig_stream:
            self.orig_stream.write(buf)
            
    def flush(self):
        "Added in because errors were occurring during testing."
        
        if self.orig_stream:
            self.orig_stream.flush()
            
"""
End support for Redirector.
"""

"Module-level variable to enforce single instance of Redirector."
_redirector = None

class Redirector:
    """
    Redirects output from stdout and stderr (e.g. those items output with
    print() statements) to the given logger. Redirection ends when instance
    is destroyed. Due to the system-level redirection, only one instance can
    exist.
    """
    # TODO: It is possible to allow multiple instances so long as we keep
    # track of all of the references.
    
    def __init__(self, logger, tee=True, levelStdOut=logging.INFO, 
                 levelStdErr=logging.ERROR):
        """
        Initializes this object. Throws RuntimeError if instance exists.
        
        @param logger A Python logger object to direct output to
        @param tee Causes printed output to go to stdout normally, as well as
                to the log
        @param levelStdOut Log level designator for stdout. Pass in None to
                not redirect stdout at all.
        @param levelStdErr Log level disginator for stderr. Pass in None to
                not redirect stderr at all.
        """
        global _redirector
        
        if _redirector:
            raise RuntimeError("Only one instance of logutil.Redirector may exist at any one time")
        
        self.origStdOut = None
        if levelStdOut:
            self.origStdOut = sys.stdout
            sys.stdout = _StreamToLogger(logger, levelStdOut, self.origStdOut if tee else None)
        self.origStdErr = None
        if levelStdErr:
            self.origStdErr = sys.stderr
            sys.stderr = _StreamToLogger(logger, levelStdErr, self.origStdErr if tee else None)
        _redirector = True
        
    def __del__(self):
        """
        Called upon object destruction. Reverts back the system streams.
        """
        global _redirector
        
        if self.origStdErr:
            sys.stderr = self.origStdErr
        if self.origStdOut:
            sys.stdout = self.origStdOut
        _redirector = False
    