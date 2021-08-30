import socket
import threading
import time

from cmd_OpenProtocol import cmd_OpenProtocol
from OpenProtocol import OpenProtocol

HOST = '10.1.10.22'
PORT = 9001
def main():
    open = OpenProtocol(HOST, PORT)
    cmd = cmd_OpenProtocol()

    open.send_msg(cmd.Communication_start())
    open.send_msg(cmd.Time_upload_request())
    open.send_msg(cmd.Vehicle_Id_Number_upload_subscribe())
    open.send_msg(cmd.Enable_tool())

if __name__ == '__main__':
    main()
