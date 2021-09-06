import socket
import threading
import time
from opensystem.cmd_OpenProtocol import cmd_OpenProtocol
from opensystem.OpenProtocol import OpenProtocol

def main():
    HOST = '10.1.10.22'
    PORT_TOOL = [
        9001, 9002, 9003, 9004,
        9005, 9006, 9007, 9008,
        9009, 9010, 9011, 9012,
        9013, 9014, 9015, 9016
    ]
    # OpenProtocol.OpenProtocol(host, port)
    open = OpenProtocol(HOST, PORT_TOOL[4])
    cmd = cmd_OpenProtocol()

    while True:
        try:
            if open.send_msg(cmd.Linking_Group_info_subscribe()) is not True:
                continue
            # if open.send_msg(cmd.Application_ID_upload_request()) is not True:
            #     continue
            # if open.send_msg(cmd.Time_upload_request()) is not True:
                # continue
            if open.send_msg(cmd.Enable_tool()) is not True:
                continue
            if open.send_msg(cmd.Last_tightening_result_data_subscribe()) is not True:
                continue
        except Exception as err:
            print(err)


if __name__ == '__main__':
    main()
