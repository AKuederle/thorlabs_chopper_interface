# -*- coding: utf-8 -*-


class RangeError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CHOPPER(object):

    """docstring for CHOPPER"""
    _intfreq_range = (1.0, 1000.0)
    _blade_range = (1.0, 7.0)
    _get_ref = (0.0, 1.0)

    def __init__(self, port=0, log=False):
        import serial
        super(CHOPPER, self).__init__()
        self.ser = serial.Serial(port)
        self.ser.timeout = 1
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.xonxoff = 0
        self.ser.rtscts = 0
        self.ser.dsrdtr = 0
        self.ser.read(100)
        self.log = log
        self.log_file = []

    def _log_write(self, string):
        if self.log is True:
            self.log_file.append(str(string))
        else:
            pass

    def get_intfreq(self):
        "get the current internal frequency"
        command = "freq?\r"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(50)  # adjust!
        self._log_write(answer)
        return answer

    def set_intfreq(self, value):
        "set the internal frequency"
        if float(value) < self._intfreq_range[0] or float(value) > self._intfreq_range[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        command = "freq={}\r".format(str(value))
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_intfreq()
        return rlvalue

    def get_blade(self):
        "get the current blade type"
        command = "blade?\r"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(50)  # adjust!
        self._log_write(answer)
        return answer

    def set_blade(self, value):
        "set the blade type"
        if float(value) < self._blade_range[0] or float(value) > self._blade_range[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        command = "blade={}\r".format(str(value))
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_intfreq()
        return rlvalue

    def get_ref(self):
        "get the current reference mode"
        command = "ref?\r"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(50)  # adjust!
        self._log_write(answer)
        return answer

    def set_ref(self, value):
        if float(value) < self._ref_range[0] or float(value) > self._ref_range[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        "set the reference mode"
        command = "ref={}\r".format(str(value))
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_intfreq()
        return rlvalue

    def get_status(self):
        "get current status (still or running)"
        command = "enable?\r"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(50)
        return answer

    def start(self):
        "send start signal"
        command = "enable = 1\r"
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_status()
        return rlvalue

    def stop(self):
        "send stop signal"
        command = "enable = 0\r"
        self._log_write(command)
        self.ser.write(command)
        rlvalue = self.get_status()
        return rlvalue

    def get_exfreq(self):
        "get current external frequency"
        command = "input?\r"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(50)
        return answer

    def get_all(self):
        all_stats = []
        all_stats.append(self.get_intfreq())
        all_stats.append(self.get_blade())
        all_stats.append(self.get_ref())
        all_stats.append(self.get_exfreq())
        all_stats.append(self.get_status())
        return all_stats

    def close(self):
        self.ser.close()
