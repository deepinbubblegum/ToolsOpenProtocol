import socket
import threading
import time
from pymodbus.compat import IS_PYTHON3, PYTHON_VERSION
if IS_PYTHON3 and PYTHON_VERSION >= (3, 4):
    import logging
    import asyncio
    from pymodbus.client.asynchronous.serial import (
        AsyncModbusSerialClient as ModbusClient)
    from pymodbus.client.asynchronous import schedulers
else:
    import sys
    sys.stderr("This example needs to be run only on python 3.4 and above")
    sys.exit(1)

# --------------------------------------------------------------------------- #
# configure the client logging
# --------------------------------------------------------------------------- #
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

UNIT = 0x01

class asyncOpenModbus():
    def __init__(self, port='/tmp/ptyp0', baudrate='9600', method='rtu'):
        self.port = port
        self.baudrate = baudrate
        self.method = method

        self.loop, self.client_init = ModbusClient(
            schedulers.ASYNC_IO, 
            port=self.port, 
            baudrate=self.baudrate,
            method=self.method
        )
        self.client = self.client_init.protocol
        self.rq = None
        self.rr = None
        thr_recv = Threading.Thread(target=self.recv)

    async def recv(self):
        print('Started Thread reading..')
        while True:
            self.rr = await self.client.read_holding_registers(1, 8, unit=UNIT)
            time.sleep(0.1)

    async def send(self, value):
        print('Sending data..')
        self.rq = await client.write_registers(1, value, unit=UNIT)