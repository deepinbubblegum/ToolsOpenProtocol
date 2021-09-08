import sys
import serial
from serial.tools import list_ports

STR_USBPORT="FT232R USB UART"

def getUSBPort():
    for port in list(list_ports.comports()):
        if port[1] == STR_USBPORT:
            return port[0]
        return None

if __name__ == "__main__":
    Port = getUSBPort()
    print(Port)
