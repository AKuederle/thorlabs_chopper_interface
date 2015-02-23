r"""chopper_controller.py provides a easy to use command line interface to control a Thorlabs optical chopper.

chopper_controller.py
=================

Provides:
1. A simple wrapper class for a a selection of USB\serial port commands to control a Thorlabs optical chopper.

The documentation of the Chopper's USB\serial interface can be found in its manual 
(Available with the product or at http://www.thorlabs.de/thorcat/18400/MC2000-Manual.pdf).
"""
__author__ = "Arne Küderle"
__copyright__ = "Copyright 2015, Arne Küderle"
__version__ = "1.0"
__maintainer__ = "Arne Küderle"
__email__ = "a.kuederle@gmail.com"

class CHOPPER(object):

    r"""Simple python wrapper class for a selection of USB\serial port commands to control a Thorlabs optical chopper.

    The class contains multiple functions to get and set the most commonly used chopper parameters. This is either done by calling the
    the functions itself (name-schema: get_*parameter* or set_*parameter*) or by using the provided namedtuples Set or Get (note the capitalisation), which are
    container for these functions.

    Usage example
    =============

        >>> import chopper_controller # makes the CHOPPER() class available in the current python session or script (make sure chopper_controller.py is in the working directory or the path)
        >>> chopper = CHOPPER() # establish the connection to the Chopper

        # Set and get using the direct function calls
        >>> print chopper.get_intefreq() # gets the current internal frequency and prints it out
        >>> chopper.set_intefreq(63) # sets the internal frequency to 63 Hz

        # Set and get using the namedtuple container
        >>> print chopper.Get.intefreq() # gets the current internal frequency and prints it out
        >>> chopper.Set.intefreq(63) # sets the internal frequency to 63 Hz


    Available functions
    ==========================
    The following list contains all parameter which can be used in combination with the set and get functions. For more detailed description
    of each parameter check the respective docstrings of the related functions or consult the chopper manual.

    Name    : Description                                        # available modes
    ==============================================================================
    intfreq : Internal reference frequency                       # get/set
    blade   : Selected blade (changes the allowed intfreq range) # get/set
    ref     : reference mode (internal or external)              # get/set
    status  : still or running                                   # get
    exfreq  : frequency of the external reference                # get

    Further functionality, which can not be described by setting or getting a parameter can be accessed by using the following functions.

    Name  : Description
    ========================
    start : starts the chopper
    stop  : stops the chopper
    close : closes the communication port

    Implementation details
    ======================
    General interface
    Despite the fact, that the chopper is connected via USB with the PC, it can be controlled using the serial package. This possible, because 
    the Chopper has a integrated USB to Serial converter and it's interface is therefore recognised as serial by the OS

    Set-function
    Before a command is send to the Chopper, it is checked, if the given value is valid for the respective parameter. This is done using the range
    information stored in the _Range namedtuple, which contains the upper and the lower limit for each parameter. (The allowed range for the internal
    frequency changes depended on the selected blade). A Set-function then sends the given parameter to the chopper.
    Right after this command the corresponding Get-function is called to check if the chopper has successfully set the parameter to its new value.
    The new value is returned to the user.

    Get-function
    The Get functions simply send a query to the chopper. The chopper than returns the value of the queried parameter. Since the returned answer contains additional characters beside the poor value
    the answer string is cut respectively and converted in an integer or float format depending of the parameter. Beside returning the value, the value is also written to the Stat tuple.

    Stat-tuple
    The Stat namedtuple contains all current known parameter values of the chopper. Please note, that this values might not reflected the real chopper state, since the values of the tuple are only updated,
    if the respective value is queried from the chopper by one of the provided Get functions. To refresh all parameter values the get_all() function can be used.

    Logging
    To log and debug the chopper communication, all traffic between this controller and the chopper can be recorded. To activate logging, the log parameter has to be set to True. This can
    be done on initialising of the connection or later on in the session.

        # on initialisation
        >>> chopper = CHOPPER(log=True)

        # later on
        >>> chopper = CHOPPER()
        >>> chopper.log = True

    If logging is enabled, all strings, send to or received from the chopper, are stored (with respective formatting for incoming and outgoing communication) as a new element of the log_file list variable.
    To save all logs of session to a file the save_log() function can be used. Please note, that this will clear the log_file variable after saving.
    """

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

    def _log_write(self, string, mode):
        from datetime import datetime
        string = str(string)
        date = str(datetime.now()).split('.')[0]
        if self.log is True:
            if mode == "read":
                msg = "<<< " + string
            elif mode == "write":
                msg = ">>> " + string
            self.log_file.append((msg, date))
        else:
            pass

    def save_log(self, file):
        with open(file, "a") as f:
            for line in self.log_file:
                f.write("[{}] {}".format(line[0], line[1]))
        self.log_file = []

    def get_intfreq(self):
        "get the current internal frequency"
        command = "freq?\r"
        self._log_write(command, mode="write")
        self.ser.write(command)
        answer = self.ser.read(15)  # adjust!
        self._log_write(answer, mode="read")
        rlvalue = float(answer[len(command):-3])
        self.Stat = self.Stat._replace(intfreq=rlvalue)
        return rlvalue

    def set_intfreq(self, value):
        "set the internal frequency"
        if float(value) < self._Range.intfreq[0] or float(value) > self._Range.intfreq[1]:
            raise ValueError("{} is out of range!".format(str(value)))
        command = "freq={}\r".format(str(value))
        self._log_write(command, mode="write")
        self.ser.write(command)
        self.ser.read(15)
        rlvalue = self.get_intfreq()
        return rlvalue

    def get_blade(self):
        "get the current blade type"
        command = "blade?\r"
        self._log_write(command, mode="write")
        self.ser.write(command)
        answer = self.ser.read(15)  # adjust!
        self._log_write(answer, mode="read")
        rlvalue = float(answer[len(command):-3])
        self.Stat = self.Stat._replace(blade=rlvalue)
        self._Range = self._Range._replace(intfreq=self._Bladerange[int(rlvalue)])
        return rlvalue

    def set_blade(self, value, ):
        "set the blade type"
        if float(value) < self._Range.blade[0] or float(value) > self._Range.blade[1]:
            raise ValueError("{} is out of range!".format(str(value)))
        command = "blade={}\r".format(str(int(value)))
        self._log_write(command, mode="write")
        self.ser.write(command)
        self.ser.read(15)
        rlvalue = self.get_intfreq()
        return rlvalue

    def get_ref(self):
        "get the current reference mode"
        command = "ref?\r"
        self._log_write(command, mode="write")
        self.ser.write(command)
        answer = self.ser.read(15)  # adjust!
        self._log_write(answer, mode="read")
        rlvalue = float(answer[len(command):-3])
        self.Stat = self.Stat._replace(ref=rlvalue)
        return rlvalue

    def set_ref(self, value):
        if float(value) < self._Range.ref[0] or float(value) > self._Range.ref[1]:
            raise ValueError("{} is out of range!".format(str(value)))
        "set the reference mode"
        command = "ref={}\r".format(str(int(value)))
        self._log_write(command, mode="write")
        self.ser.write(command)
        self.ser.read(15)
        rlvalue = self.get_ref()
        return rlvalue

    def get_status(self):
        "get current status (still or running)"
        command = "enable?\r"
        self._log_write(command, mode="write")
        self.ser.write(command)
        answer = self.ser.read(15)
        self._log_write(answer, mode="read")
        rlvalue = float(answer[len(command):-3])
        self.Stat = self.Stat._replace(status=rlvalue)
        return rlvalue

    def get_exfreq(self):
        "get current external frequency"
        command = "input?\r"
        self._log_write(command, mode="write")
        self.ser.write(command)
        answer = self.ser.read(15)
        self._log_write(answer, mode="read")
        rlvalue = float(answer[len(command):-3])
        self.Stat = self.Stat._replace(exfreq=rlvalue)
        return rlvalue

    def start(self):
        "send start signal"
        command = "enable=1\r"
        self._log_write(command, mode="write")
        self.ser.write(command)

    def stop(self):
        "send stop signal"
        command = "enable=0\r"
        self._log_write(command, mode="write")
        self.ser.write(command)

    def get_all(self):
        for command in self.Get[:-1]:
            command()
        return self.Stat

    def close(self):
        self.ser.close()
