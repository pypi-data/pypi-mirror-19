# coding:utf-8

import os
import signal

from nose.plugins import Plugin


class NoseSigterm(Plugin):
    name = 'sigterm'
    SIGNALS = [signal.SIGTERM]

    def options(self, parser, env=os.environ):
        super(NoseSigterm, self).options(parser, env=env)

    def configure(self, options, conf):
        super(NoseSigterm, self).configure(options, conf)
        if not self.enabled:
            return

    def _raise_keyboard_interrupt(self, signum, frame):
        # The signal handler should be removed in case KeyboardInterrupt
        # is being caught by the code somewhere, which would then require
        # SIGKILL to terminate. This allows a subsequent SIGTERM to terminate.
        self._remove_signal_handler(signum)
        raise KeyboardInterrupt()

    def _remove_signal_handler(self, signum):
        signal.signal(signum, signal.SIG_DFL)

    def begin(self):
        for s in self.SIGNALS:
            signal.signal(s, self._raise_keyboard_interrupt)
