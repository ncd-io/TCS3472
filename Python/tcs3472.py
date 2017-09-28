#include "Particle.h"

# Command register
TCS3472_COMMAND_REG = 0x80

# Enable register
TCS3472_ENABLE_REG = 0x00

TCS3472_ENABLE_INT = 0xA0
TCS3472_ENABLE_WAIT = 0x08
TCS3472_ENABLE_RGBC = 0x02
TCS3472_ENABLE_POWER = 0x01


# Integration timing register, integration time works in 2.4ms increments STARTING at = 0xF6, i.e. writing a  will set the integration time to 24ms
TCS3472_TIMING_REG = 0x01

# Wait time register, also works in 2.4ms increments exactly as above, unless the WLONG flag is set, in which case the time is 12x longer
TCS3472_WAIT_REG = 0x03


# Configuration register, only used for the WLONG flag
TCS3472_CONFIG_REG = 0x0D
TCS3472_WLONG = 0x02


# Control register, used for setting gain
TCS3472_CONTROL_REG = 0x0F

TCS3472_AGAIN_1 = 0x00
TCS3472_AGAIN_4 = 0x01
TCS3472_AGAIN_16 = 0x02
TCS3472_AGAIN_60 = 0x03


# Status register
TCS3472_STATUS_REG = 0x13

# integration cycles have completed
TCS3472_AVALID = 0x01


TCS3472_DATA_REGISTER_0 = 0x14

class TCS3472():
	def __init__(self, smbus, kwargs = {}):
		self.__dict__.update(kwargs)
		if not hasattr(self, 'address'):
			self.address = 0x29
		if not hasattr(self, 'wait_enable'):
			self.wait_enable = TCS3472_ENABLE_WAIT
		if not hasattr(self, 'gain'):
			self.gain = TCS3472_AGAIN_4
		if not hasattr(self, 'wlong'):
			self.wlong = False
		if not hasattr(self, 'wait_time'):
			self.wait_time = 0x00
		if not hasattr(self, 'timing'):
			self.timing = 0x00
		self.smbus = smbus

		self.smbus.write_byte_data(self.address, TCS3472_COMMAND_REG | TCS3472_ENABLE_REG, self.wait_enable | TCS3472_ENABLE_RGBC | TCS3472_ENABLE_POWER)
		self.smbus.write_byte_data(self.address, TCS3472_COMMAND_REG | TCS3472_CONTROL_REG, self.gain)
		self.smbus.write_byte_data(self.address, TCS3472_COMMAND_REG | TCS3472_TIMING_REG, self.timing)
		self.smbus.write_byte_data(self.address, TCS3472_COMMAND_REG | TCS3472_WAIT_REG, self.wait_time)

		if self.wlong:
				self.smbus.write_byte_data(self.address, TCS3472_COMMAND_REG | TCS3472_CONFIG_REG, TCS3472_WLONG)

	def get_readings(self):
		readings = self.smbus.read_i2c_block_data(self.address, TCS3472_COMMAND_REG | TCS3472_DATA_REGISTER_0, 8)

		read_array = {'clear': False, 'red': False, 'green': False, 'blue': False}
		read_array['clear'] = readings[0] + (readings[1] << 8)
		read_array['red'] = readings[2] + (readings[3] << 8)
		read_array['green'] = readings[4] + (readings[5] << 8)
		read_array['blue'] = readings[6] + (readings[7] << 8)

		if hasattr(self, 'white_balance'):
			read_array['red'] = read_array['red'] - self.white_balance['red']
			read_array['green'] = read_array['green'] - self.white_balance['green']
			read_array['blue'] = read_array['blue'] - self.white_balance['blue']


		return read_array

	def unset_white_balance(self):
		self.white_balance = {'red': 0, 'green': 0, 'blue': 0}

	def set_white_balance(self):
		readings = self.smbus.read_i2c_block_data(self.address, TCS3472_COMMAND_REG | TCS3472_DATA_REGISTER_0, 8)

		read_array = {'clear': False, 'red': False, 'green': False, 'blue': False}
		read_array['red'] = readings[2] + (readings[3] << 8)
		read_array['green'] = readings[4] + (readings[5] << 8)
		read_array['blue'] = readings[6] + (readings[7] << 8)
		base = min(read_array['red'], read_array['green'], read_array['blue'])
		read_array['red'] = read_array['red'] - base
		read_array['green'] = read_array['green'] - base
		read_array['blue'] = read_array['blue'] - base
		self.white_balance = read_array

	def to_rgb_bright(self, read_array):
		ratio = float(65535) / float(max(read_array['red'], read_array['green'], read_array['blue']))
		read_array['red'] = int(ratio*read_array['red'] / 256)
		read_array['green'] = int(ratio*read_array['green'] / 256)
		read_array['blue'] = int(ratio*read_array['blue'] / 256)

		return read_array

	def to_rgb(self, read_array):
		read_array['red'] = int(read_array['red'] / 256)
		read_array['green'] = int(read_array['green'] / 256)
		read_array['blue'] = int(read_array['blue'] / 256)

		return read_array
