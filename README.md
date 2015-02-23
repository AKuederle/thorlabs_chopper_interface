## thorlabs_chopper_interface

Thorlabs_chopper_interface is a pythonbased wrapper for a selction of serial port commands to control a Thorlabs "MC2000 Optical Chopper".

It Provides:

1. A simple wrapper class for a a selection of USB\serial port commands to control a Thorlabs "MC2000 Optical Chopper".

The documentation of the Chopper's USB\serial interface can be found in its manual (Available with the product or at http://www.thorlabs.de/thorcat/18400/MC2000-Manual.pdf).

### Usage
The chopper_controller.py includes a CHOPPER class. It can be used in an interactive Python shell or in a arbitrary python script by importing the module and creating an instance of the class.
The provided functions (see class docstring) can than be used to control the laser.

#### Example

```python
import chopper_controller # makes the CHOPPER() class available in the current python session or script (make sure chopper_controller.py is in the working directory or the path)
chopper = CHOPPER() # establish the connection to the chopper

# Set and get using the direct function calls
print chopper.get_intfreq() # gets the current internal frequency and prints it out
chopper.set_intfreq(63) # sets the internal frequency to 63 Hz

# Set and get using the namedtuple container
print chopper.Get.intfreq() # gets the current internal frequency and prints it out
chopper.Set.intfreq(63) # sets the internal frequency to 63 Hz
```


### License
thorlabs_chopper_interface is published under the MIT license.
=======
## thorlabs_chopper_interface

Thorlabs_chopper_interface is a pythonbased wrapper for a selction of serial port commands to control a Thorlabs "MC2000 Optical Chopper".

It Provides:

1. A simple wrapper class for a a selection of USB\serial port commands to control a Thorlabs "MC2000 Optical Chopper".

The documentation of the Chopper's USB\serial interface can be found in its manual (Available with the product or at http://www.thorlabs.de/thorcat/18400/MC2000-Manual.pdf).

### Usage
The chopper_controller.py includes a CHOPPER class. It can be used in an interactive Python shell or in a arbitrary python script by importing the module and creating an instance of the class.
The provided functions (see class docstring) can than be used to control the chopper.

#### Example

```python
import chopper_controller # makes the CHOPPER() class available in the current python session or script (make sure chopper_controller.py is in the working directory or the path)
chopper = CHOPPER() # establish the connection to the chopper

# Set and get using the direct function calls
print chopper.get_intfreq() # gets the current internal frequency and prints it out
chopper.set_intfreq(63) # sets the internal frequency to 63 Hz

# Set and get using the namedtuple container
print chopper.Get.intfreq() # gets the current internal frequency and prints it out
chopper.Set.intfreq(63) # sets the internal frequency to 63 Hz
```


### License
thorlabs_chopper_interface is published under the MIT license.

