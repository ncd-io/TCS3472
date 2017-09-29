# About

This Library is intended for use with any TCS347 board available from ncd.io

### Developer information
NCD has been designing and manufacturing computer control products since 1995.  We have specialized in hardware design and manufacturing of Relay controllers for 20 years.  We pride ourselves as being the industry leader of computer control relay products.  Our products are proven reliable and we are very excited to support Particle.  For more information on NCD please visit ncd.io

### Requirements
- The Python SMBus Module: https://pypi.python.org/pypi/smbus-cffi/
- An I2C connection to the board
- Knowledge base for developing and programming with Python.

### Version
1.0.0

### How to use this library

The libary must be imported into your application and an I2C bus must be created with the SMBus module.

Once the library is imported and the I2C Bus created you can create a TCS3472 object, pass it the I2C Bus and start to communicate to the chip.  You can optionally pass in a kwarg to the object that contains many configuration options such as address, wait_enable, gain, wlong, wait_time, and timing. Of particular import is the address and gain. We recommend a value of 1 or 2 in room with standard illumination.

The default values for these configuration option are:
{'address': 0x29, 'wait_enable': 0x08, 'gain': 0x01, 'wlong': False, 'wait_time': 0x00, 'timing': 0x00}

### Publicly accessible methods
```cpp
get_readings()
```
>This function returns the readings of the sensor in a keyed array. The keys are 'red', 'green', 'blue', and 'clear'.

```cpp
set_white_balance()
```
>This function creates a kind of zero point for readings to account for ambient lighting being off white. 

```cpp
unset_white_balance()
```
>This function gets rid of any white balance being used in the object. 

```cpp
to_rgb_bright(reading_array)
```
>This accepts  the array returned by get_readings() and returns a keyed array of value from 0-255. The array keys are 'red', 'green', 'blue', and 'clear'.
>The purpose is the give you an RGB readings that will ramp up the brightness of the color to take the gain out of the equation.

```cpp
to_rgb(reading_array)
```
>This accepts  the array returned by get_readings() and returns a keyed array of value from 0-255. The array keys are 'red', 'green', 'blue', and 'clear'.
>The purpose is the give you an RGB readings that will accurately display what color the sensor is seeing.
