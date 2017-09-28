import time
import smbus
import tcs3472
# Get I2C bus, this is I2C Bus 1
bus = smbus.SMBus(1)

#kwargs is a Python set that contains the address of your device as well as additional device and calibration values.
#kwargs does not have to be populated as every value is optional and will be replaced with a default value if not is specified.

#below is an example of a kwarg declaration that is populated with all of the default values for each user configurable property
#refer to the datasheet for this chip to calculate what values you should be using for your project.
kwargs = {'address': 0x29, 'wait_enable': 0x08, 'gain': 0x01, 'wlong': False, 'wait_time': 0x00, 'timing': 0x00}
#create the MCP3428 object from the MCP3428 library
#the object requires that you pass it the bus object so that it can communicate and share the bus with other chips if necessary
board = tcs3472.TCS3472(bus, kwargs)

while True :
    #get rgbc readings in an array keyed by red green blue clear
    all_readings = board.get_readings()
    print 'All Readings:'
    print all_readings

    # get the rgb values of the values passed. does not effect clear
    doctored_readings = board.to_rgb(all_readings)
    print 'doctored readings'
    print doctored_readings

    # get the brightest version of the color detected possible
    adjusted_doctored_readings = board.to_rgb(all_readings)
    print 'bright rgb'
    print adjusted_doctored_readings

    print '---White Balance Set---'
    # set white balance to normalize color readings and make them read back equal.
    # does not effect clear
    # white balance is set by the color readings at the time of the command execution
    board.set_white_balance()

    all_readings = board.get_readings()
    print 'All Readings:'
    print all_readings

    doctored_readings = board.to_rgb(all_readings)
    print 'doctored readings'
    print doctored_readings

    adjusted_doctored_readings = board.to_rgb(all_readings)
    print 'bright rgb'
    print adjusted_doctored_readings

    #unset white balance to get raw values
    board.unset_white_balance()

    print '---'
    print ''
    time.sleep(5)
