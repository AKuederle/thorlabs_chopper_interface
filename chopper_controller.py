# -*- coding: utf-8 -*-


class RangeError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class CHOPPER(object):
	"""docstring for CHOPPER"""
	def __init__(self, port=0, log=False):
		import serial
		super(CHOPPER, self).__init__()
		