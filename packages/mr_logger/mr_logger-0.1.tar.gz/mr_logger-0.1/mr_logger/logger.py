# -*- coding: utf-8 -*-
#!/usr/bin/python

from termcolor import colored


TYPES = ['info', 'warn', 'err', 'ok', 'def']

INFO = TYPES[0]
WARN = TYPES[1]
ERR = TYPES[2]
OK = TYPES[3]
DEF = TYPES[4]

PREFIXES = {INFO: '[INFO]: ', WARN: '[WARN]: ',
           ERR: '[❌]: ', OK: '[✔]: ', DEF: '[✴] ▶▶▶ '}

COLORS = {INFO: 'cyan', WARN: 'yellow', ERR: 'red',
          OK: 'green', DEF: 'white'}


class Logger:
    type_info = INFO
    type_warn = WARN
    type_err = ERR
    type_ok = OK
    type_default = DEF

    def __init__(self):
        pass

    @staticmethod
    def _get_prefix(msg_type):
        return PREFIXES[msg_type]

    @staticmethod
    def _get_color(msg_type):
        return COLORS[msg_type]

    def _prefix_text(self, msg_type, text):
        return self._get_prefix(msg_type=msg_type) + str(text)

    def _get_ready_text(self, msg_type, text):
        color = COLORS[msg_type]
        text = self._prefix_text(msg_type=msg_type, text=text)
        txt_colored = colored(text, color)
        return txt_colored

    def info(self, text):
        print((self._get_ready_text(msg_type=self.type_info, text=text)))

    def warn(self, text):
        print((self._get_ready_text(msg_type=self.type_warn, text=text)))

    def err(self, text):
        print((self._get_ready_text(msg_type=self.type_err, text=text)))

    def ok(self, text):
        print((self._get_ready_text(msg_type=self.type_ok, text=text)))

    def log(self, text):
        print((self._get_ready_text(msg_type=self.type_default, text=text)))
