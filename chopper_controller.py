# -*- coding: utf-8 -*-


class RangeError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CHOPPER(object):
    """docstring for CHOPPER"""
    from collections import namedtuple
    _blades = ["MC1F2", "MC1F6", "MC1F10", "MC1F15", "MC1F30", "MC1F60", "MC1F100", "MC1F57"]
    _control = namedtuple("control", ["intfreq", "blade", "ref"])
    _state = namedtuple("state", ["status", "intfreq", "exfreq", "blade", "ref"])
    _query = namedtuple("query", ["status", "intfreq", "exfreq", "blade", "ref", "all"])
    _bladerange = namedtuple("bladerange", _blades)


    def __init__(self, port=3, log=False):
        import serial
        super(CHOPPER, self).__init__()
        self.ser = serial.Serial(port)
        self.ser.baudrate = 115200
        self.ser.timeout = 1
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.xonxoff = 0
        self.ser.rtscts = 0
        self.ser.dsrdtr = 0
        self.ser.write("\r")
        self.ser.read(100)
        self.log = log
        self.log_file = []
        self._Range = self._control(intfreq=(1.0, 1000.0), blade=(0.0, 6.0), ref=(0.0, 1.0))
        self._Bladerange = self._bladerange(MC1F2=(1.0, 99.0), MC1F6=(0.0, 0.0), MC1F10=(20.0, 1000.0), MC1F15=(30.0, 1500.0), MC1F30=(60.0, 3000.0), MC1F60=(120.0, 6000.0), MC1F100=(0.0, 0.0), MC1F57=(10.0, 500.0))
        self.Set = self._control(intfreq=self.set_intfreq, blade=self.set_blade, ref=self.set_ref)
        self.Get = self._query(status=self.get_status, intfreq=self.get_intfreq, exfreq=self.get_exfreq, blade=self.get_blade, ref=self.get_ref, all=self.get_all)
        self.Stat = self._state(status=None, intfreq=None, exfreq=None, blade=None, ref=None)
        self.Get.all()

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
        answer = self.ser.read(15)  # adjust!
        self._log_write(answer)
        rlvalue = float(answer[len(command):-3])
        self.Stat = self.Stat._replace(intfreq=rlvalue)
        return rlvalue

    def set_intfreq(self, value):
        "set the internal frequency"
        if float(value) < self._Range.intfreq[0] or float(value) > self._Range.intfreq[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        command = "freq={}\r".format(str(value))
        self._log_write(command)
        self.ser.write(command)
        self.ser.read(15)
        rlvalue = self.get_intfreq()
        return rlvalue

    def get_blade(self):
        "get the current blade type"
        command = "blade?\r"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(15)  # adjust!
        self._log_write(answer)
        rlvalue = float(answer[len(command):-3])
        self.Stat = self.Stat._replace(blade=rlvalue)
        self._Range = self._Range._replace(intfreq=self._Bladerange[int(rlvalue)])
        return rlvalue

    def set_blade(self, value, ):
        "set the blade type"
        if float(value) < self._Range.blade[0] or float(value) > self._Range.blade[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        command = "blade={}\r".format(str(int(value)))
        self._log_write(command)
        self.ser.write(command)
        self.ser.read(15)
        rlvalue = self.get_intfreq()
        return rlvalue

    def get_ref(self):
        "get the current reference mode"
        command = "ref?\r"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(15)  # adjust!
        self._log_write(answer)
        rlvalue = float(answer[len(command):-3])
        self.Stat = self.Stat._replace(ref=rlvalue)
        return rlvalue

    def set_ref(self, value):
        if float(value) < self._Range.ref[0] or float(value) > self._Range.ref[1]:
            raise RangeError("{} is out of range!".format(str(value)))
        "set the reference mode"
        command = "ref={}\r".format(str(int(value)))
        self._log_write(command)
        self.ser.write(command)
        self.ser.read(15)
        rlvalue = self.get_ref()
        return rlvalue

    def get_status(self):
        "get current status (still or running)"
        command = "enable?\r"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(15)
        rlvalue = float(answer[len(command):-3])
        self.Stat = self.Stat._replace(status=rlvalue)
        return rlvalue

    def get_exfreq(self):
        "get current external frequency"
        command = "input?\r"
        self._log_write(command)
        self.ser.write(command)
        answer = self.ser.read(15)
        rlvalue = float(answer[len(command):-3])
        self.Stat = self.Stat._replace(exfreq=rlvalue)
        return rlvalue

    def start(self):
        "send start signal"
        command = "enable=1\r"
        self._log_write(command)
        self.ser.write(command)

    def stop(self):
        "send stop signal"
        command = "enable=0\r"
        self._log_write(command)
        self.ser.write(command)

    def get_all(self):
        for command in self.Get[:-1]:
            print command
            command()
        return self.Stat

    def close(self):
        self.ser.close()
