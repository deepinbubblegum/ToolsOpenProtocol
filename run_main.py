import socket
import threading
import time
from opensystem.cmd_OpenProtocol import cmd_OpenProtocol
from opensystem.OpenProtocol import OpenProtocol
import sqlite3
from lib.modbus import TrayModbus

def QuerySQL(SQL):
    conn = sqlite3.connect('./database/openprotocol.db')
    cur = conn.cursor()
    cur.execute(SQL)
    res_data = cur.fetchall()
    conn.commit()
    conn.close()
    return res_data


def main():
    HOST = '10.1.10.22'
    PORT_TOOL = [
        9001, 9002, 9003, 9004,
        9005, 9006, 9007, 9008
    ]

    open = OpenProtocol(HOST, PORT_TOOL[4])
    cmd = cmd_OpenProtocol()
    tray_modbus = TrayModbus(
        method='rtu', 
        port='/dev/ttyUSB0',
        timeout=1,
        baudrate=19200
    )
    counting_step = 1
    while True:
        checked = 0
        old_position = None
        SQL_txt = 'SELECT * FROM Step WHERE ID_Link_step = 1'
        res_step = QuerySQL(SQL_txt)
        if open.send_msg(cmd.Disable_tool()) is not True:
            continue
        open.SetData(None)

        if open.send_msg(cmd.Vehicle_Id_Number_upload_subscribe()) is True:
            res_VIN_CODE = open.Get_VIN_Number_CODE()
            if res_VIN_CODE is None:
                continue
            print(res_VIN_CODE)
            while True:
                loop = len(res_step)
                try:
                    res_step[checked][3]
                except Exception as e:
                    break

                print(res_step[checked][3])
                regis = tray_modbus.regisRead(res_step[checked][3], 8)
                print(regis)

                if loop == checked:
                    checked = 0
                    print('exit loop')
                    break
                open.Set_VIN_Number_CODE(None)
                open.send_msg(cmd.Enable_tool())
                # print('Enable_tool')
                open.send_msg(cmd.Last_tightening_result_data_subscribe())
                res_lastData = open.GetData()
                if res_lastData is not None:
                    # print(res_lastData['Tightening_Status'])
                    if int(res_lastData['Tightening_Status']):
                        checked += 1
                        print('Tightening :OK')
                    else:
                        print('Tightening :NOK')
                        if old_position != res_lastData['Batch_counter']:
                            checked += 1
                    old_position = res_lastData['Batch_counter']
                    open.SetData(None)
                time.sleep(0.01)
            print('end cycle position')
        time.sleep(0.01)
if __name__ == '__main__':
    main()