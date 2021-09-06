import socket
import threading
import time
from opensystem.cmd_OpenProtocol import cmd_OpenProtocol
from opensystem.OpenProtocol import OpenProtocol
import sqlite3

def QuerySQL(SQL):
    conn = sqlite3.connect('./database/openprotocol.db')
    cur = conn.cursor()
    cur.execute(SQL)
    res_data = cur.fetchall()
    conn.commit()
    conn.close()
    return res_data

    #  SQL_txt = 'SELECT * FROM Step WHERE ID_Link_step = 1'
# def ToolsPools(HOST, PORT):
#     open = OpenProtocol(HOST, PORT)
#     cmd = cmd_OpenProtocol()
#     while True:
#         try:
#             # if open.send_msg(cmd.Linking_Group_info_subscribe()) is not True:
#             #     continue
#             if open.send_msg(cmd.Application_ID_upload_request()) is not True:
#                 continue
#             # if open.send_msg(cmd.Time_upload_request()) is not True:
#                 # continue
#             if open.send_msg(cmd.Enable_tool()) is not True:
#                 continue
#             if open.send_msg(cmd.Last_tightening_result_data_subscribe()) is not True:
#                 continue
#             time.sleep(0.2)
#         except Exception as err:
#             print(err)


def main():
    HOST = '10.1.10.22'
    PORT_TOOL = [
        9001, 9002, 9003, 9004,
        9005, 9006, 9007, 9008
    ]

    # thr_pool = []
    # for Port in PORT_TOOL:
    #     thr_pool.append(
    #         threading.Thread(target=ToolsPools, args=(HOST, Port,))
    #     )

    # for thr in thr_pool:
    #     thr.start()

    # OpenProtocol.OpenProtocol(host, port)
    open = OpenProtocol(HOST, PORT_TOOL[4])
    cmd = cmd_OpenProtocol()

    while True:
        try:
            # if open.send_msg(cmd.Linking_Group_info_subscribe()) is not True:
            #     continue
            # if open.send_msg(cmd.Application_ID_upload_request()) is not True:
            #     continue
            # if open.send_msg(cmd.Time_upload_request()) is not True:
                # continue
            if open.send_msg(cmd.Disable_tool()) is not True:
                continue
            if open.send_msg(cmd.Vehicle_Id_Number_upload_subscribe()) is not True:
                continue
            if open.send_msg(cmd.Enable_tool()) is not True:
                continue
            if open.send_msg(cmd.Last_tightening_result_data_subscribe()) is not True:
                continue
        except Exception as err:
            print(err)


if __name__ == '__main__':
    main()
