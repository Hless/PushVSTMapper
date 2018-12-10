''' Logger class '''

import os
from .config import APP_DIR, LOG_ENABLED

class Logger:
    ''' Class handles various logging purposes '''
    _log_handles = {}

    def __init__(self):
        pass

    def _get_log_file(self, name):
        if name in self._log_handles:
            return self._log_handles[name]

        log_h = open(os.path.join(APP_DIR, name + '.log'), 'w')
        self._log_handles[name] = log_h
        return log_h

    def write(self, msg, name=None):
        ''' Writes message to the log '''
        if not LOG_ENABLED:
            return

        if not name:
            name = 'main'

        msg = str(msg)

        self._get_log_file(name).write(msg + '\n')
        self._get_log_file(name).flush()

    def debug(self, msg, name=None):
        ''' Write debug message to log '''
        self.write('DEBUG: ' + str(msg), name)

    def info(self, msg, name=None):
        ''' Write info message to log '''
        self.write('INFO: ' + str(msg), name)

    def error(self, msg, name=None):
        ''' Write error message to log '''
        self.write('ERROR: ' + str(msg), name)


LOGGER = Logger()
