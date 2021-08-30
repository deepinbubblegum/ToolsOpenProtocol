import socket
import threading
import time
from cmd_OpenProtocol import cmd_OpenProtocol
from data_info import Data_info

class OpenProtocol:
    def __init__(self, host, port):
        self.server = host
        self.port = port
        self.dataInfo = Data_info()
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.server, self.port))
        self.isClose = False
        self.t_recvMsg = threading.Thread(target=self.recv_msg)
        self.t_recvMsg.start()

        # parameter
        self.cluster_number = None

    def recv_filter(self, recv_msg):
        recv_msg = recv_msg.decode('ascii')
        recv_msg = recv_msg.split(" ")
        array_list = list(filter(None, recv_msg))
        return array_list

    def send_msg(self, send_msg):
        send_msg = send_msg.encode('ascii')
        self.conn.send(send_msg)

    def msg_operation(self, msg):
        print(msg)

    def recv_msg(self):
        while self.isClose is not True:
            recv_msg = self.conn.recv(1024)
            if recv_msg:
                recv_msg = self.recv_filter(recv_msg)
                self.msg_operation(recv_msg)
                # if recv_msg[1] is not None:
                #     if recv_msg[1] == self.dataInfo.isCommunication_stop:
                #         self.close()

    def close(self):
        self.isClose = True
        self.conn.close()
