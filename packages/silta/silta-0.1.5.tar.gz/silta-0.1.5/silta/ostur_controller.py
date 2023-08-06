''' Silta STM32F407 Discovery Bridge

--- Supported Pins
I2C:
* PB6 - I2C1 SCL
* PB7 - I2C1 SDA

SPI:
N/A

ADC:
N/A

DAC:
N/A

PWM:
N/A

GPIO:
N/A
'''

import serial
import string
import sys
import re
from silta import Silta

class bridge(Silta):
    ''' Silta STM32F407 Discovery Bridge '''

    __pinModes = {
        'input': 'in',
        'output': 'outpp',
        'output-od': 'outod',
        'analog': 'analog'
    }

    __pullModes = {
        'up': 'pullup',
        'down': 'pulldown',
        'none': 'nopull'
    }

    __adcs = {}

    __dacs = {}

    __pwms = {}

    __ADC_MAX_VOLTAGE = 3.0
    __ADC_MAX_VAL = 4095

    __DAC_MAX_VOLTAGE = 3.0
    __DAC_MAX_VAL = 4095

    DEBUG = False

    def __init__(self, serial_device, baud_rate=None):
        ''' Initialize Silta STM32F407 Bridge

            Arguments:
            USB serial device path (e.g. /dev/ttyACMX, /dev/cu.usbmodemXXXXX)
        '''

        self.stream = None

        self.lastcspin = None

        try:
            self.stream = serial.Serial()
            self.stream.port = serial_device
            self.stream.timeout = 0.1
            if baud_rate:
                self.stream.baudrate = baud_rate
            self.stream.open()
        except OSError:
            raise IOError('could not open ' + serial_device)

        if self.stream:
            self.stream.flush()

        # Get device serial number and save it
        line = self.__send_cmd('sn\n')
        result = line.strip().split(' ')

        if result[0] == 'OK':
            self.serial_number = ''.join(result[1:])
        else:
            self.serial_number = None
            print('Warning: Could not read device serial number.')
            print('You might want to update firmware on your board')

        # Get device serial number and save it
        line = self.__send_cmd('version\n')
        result = line.strip().split(' ')

        if result[0] == 'OK':
            self.firmware_version = result[1]
        else:
            self.firmware_version = None
            print('Warning: Could not read device firmware version.')
            print('You might want to update firmware on your board')


    def close(self):
        ''' Disconnect from USB-serial device. '''
        self.stream.close()

    # Send terminal command and wait for response
    def __send_cmd(self, cmd):
        self.stream.write(cmd + '\n')
        if self.DEBUG is True:
            print 'CMD : ' + cmd

        line = self.stream.readline()
        if self.DEBUG is True:
            print 'RESP: ' + line,

        return line

    # Set I2C Speed
    def i2c_speed(self, speed):
            return False

    # I2C Transaction (wbytes is a list of bytes to tx)
    def i2c(self, addr, rlen, wbytes = []):
        ''' I2C Transaction (write-then-read)

            Arguments:
            addr - 8 bit I2C address
            rlen - Number of bytes to read
            wbytes - List of bytes to write

            Return value:
            Integer with error code
            or
            List with read bytes (or empty list if write-only command)
        '''

        rbytes = []
        cmd = 'i2c ' + format(addr, '02X') + ' ' + str(rlen)

        for byte in wbytes:
            cmd += format(byte, ' 02X')

        line = self.__send_cmd(cmd)

        result = line.strip().split(' ')

        if result[0] == 'OK':
            for byte in result[1:]:
                rbytes.append(int(byte, 16))
        else:
            rbytes = int(result[1])

        return rbytes
