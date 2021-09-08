#!/usr/bin/env python3
import minimalmodbus
import serial

class TrayModbus():
    def __init__(self, port='/dev/ttyUSB0', baudrate=19200, bytesize = 8, parity=serial.PARITY_NONE, stopbits=1, timeout=0.05):
        self.instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 0x01)  # port name, slave address (in decimal)
        self.instrument.serial.port                     # this is the serial port name
        self.instrument.serial.baudrate = 19200         # Baud
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity   = serial.PARITY_NONE
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout  = 0.05          # seconds

        self.instrument.address                         # this is the slave address number
        self.instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
        self.instrument.clear_buffers_before_each_transaction = True

    def write_register(self, address, value, mode=1):
        self.instrument.write_register(address, value, mode)

    def read_register(self, address, mode=1):
        res_value = self.instrument.read_register(address, mode)  # Registernumber, number of decimals
        return res_value

    def close(self):
        self.instrument.serial.close()