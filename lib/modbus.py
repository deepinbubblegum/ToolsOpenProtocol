from pymodbus.client.sync import ModbusSerialClient as ModbusClient

import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.WARNING)

class TrayModbus():
    def __init__(self, method='rtu', port='/dev/ptyp0',timeout=1,baudrate=9600):
        self.client = ModbusClient(
            method=method, 
            port=port,
            timeout=timeout,
            baudrate=baudrate
        )
        self.client.connect()

    def regisWrites(self, address, value, unit):
        rq = self.client.write_registers(address, value, unit)
        return rq

    def regisRead(self, address, value, unit):
        rr = self.client.read_holding_registers(address, value, unit)
        return rr

    def disconnect(self):
        self.client.close()