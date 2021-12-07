#!/usr/bin/python3
import json
import os
from time import sleep
import logging


CHROMIUM_STATE = '/home/{user}/.config/chromium/Local State'
DEFAULT_SCRIPT = '/home/{user}/refresh-chromium.sh'
DEFAULT_POLLING_SECS = 10.
DEFAULT_USER = 'pi'

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


class awSnap:
    def __init__(self, user=DEFAULT_USER, pollingSecs=DEFAULT_POLLING_SECS, script=DEFAULT_SCRIPT):
        self._user = user
        self._pollingSecs = pollingSecs
        self._script = script
        self._stateFileName = CHROMIUM_STATE.format(user=user)
        self._crashLoop()

    def _getCrashCount(self):
        """Read the state file (in json format) that chromium stores in the
        running users directory.  Retrieve the render_crash_count which indicates
        an 'aw snap!' message."""

        try:
            with open(self._stateFileName) as f:
                state = json.load(f)
                return state['user_experience_metrics']['stability']['renderer_crash_count']

        except Exception as e:
            logging.debug(e)
            return None

    def _crashLoop(self):
        """Retrieve the browser crash counter and poll for changes (growth).
        If/when the crash count changes run a script.
        """

        logging.info('Retrieving Base Crash Count')
        baseCrashCount = 0
        while True:
            baseCrashCount = self._getCrashCount()
            if baseCrashCount != None:
                break
            sleep(self._pollingSecs)
        logging.info('Base Crash Count is %d' % baseCrashCount)

        logging.info('Starting main loop')
        while True:
            crashCount = self._getCrashCount()
            if crashCount != None and crashCount > baseCrashCount:
                logging.info('Crash detected: crash number: {count}'.format(count=crashCount))
                baseCrashCount = crashCount
                os.system(self._script)
            sleep(self._pollingSecs)

        logging.info('Exited')

if __name__ == '__main__':
    awsnap = awSnap()


