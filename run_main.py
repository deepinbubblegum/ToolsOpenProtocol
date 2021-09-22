import socket
import threading
import time
import serial
import sqlite3
from system.cmd_OpenProtocol import cmd_OpenProtocol
from system.OpenProtocol import OpenProtocol
from system.socket_tray import socket_tray
from lib.traySocket_v2 import TrayModbusV2

def QuerySQL(SQL):
    conn = sqlite3.connect('./database/openprotocol.db')
    cur = conn.cursor()
    cur.execute(SQL)
    res_data = cur.fetchall()
    conn.commit()
    conn.close()
    return res_data

def init_socket_led():
    pass

def main():
    HOST = '10.1.10.22'
    PORT_TOOL = [
        9001, 9002, 9003, 9004,
        9005, 9006, 9007, 9008
    ]

    open = OpenProtocol(HOST, PORT_TOOL[3])
    cmd = cmd_OpenProtocol()
    tray_modbus = TrayModbusV2(
        port='/dev/ttyUSB0', 
        device=0x01, 
        baudrate=9600, 
        bytesize = 8, 
        parity=serial.PARITY_NONE, 
        stopbits=1, 
        timeout=0.05
    )
    socket_hole = socket_tray(tray_modbus, open)
    
    while True:
        checked = 0
        old_position = None
        SQL_txt = 'SELECT * FROM Step WHERE ID_Link_step = 1 ORDER BY Step_number ASC'
        res_step = QuerySQL(SQL_txt)
        if open.send_msg(cmd.Disable_tool()) is not True:
            time.sleep(0.2)
            continue
        open.SetData(None)
        
        # { #example data from mPro400gc
        # 'Linking_Group_ID': '01', 'Linking_Group_status': '0', 
        # 'Linking_Group_batch_mode': '1', 'Linking_Group_batch_size': '0005', 
        # 'Linking_Group_batch_counter': '0000', 
        # 'Time_stamp': datetime.datetime(2021, 9, 11, 18, 23, 46)
        # }
        
        # socket_hole.set_init_Socket(2, 0x00F)
        open.send_msg(cmd.Linking_Group_info_subscribe())
        # init_socket_led()

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
                                
                if loop == checked:
                    checked = 0
                    print('exit loop')
                    break

                open.Set_VIN_Number_CODE(None)
                
                socket_hole.set_socket_pickup(res_step[checked][3])
                
                open.send_msg(cmd.Last_tightening_result_data_subscribe())
                res_lastData = open.GetData()
                if res_lastData is not None:
                    # print(res_lastData['Tightening_Status'])
                    if int(res_lastData['Tightening_Status']):
                        open.send_msg(cmd.Disable_tool())
                        checked += 1
                        socket_hole.set_NextPosition()
                        print('Tightening :OK')
                    else:
                        print('Tightening :NOK')
                        if old_position != res_lastData['Batch_counter']:
                            open.send_msg(cmd.Disable_tool())
                            checked += 1
                            socket_hole.set_NextPosition()
                    old_position = res_lastData['Batch_counter']
                    open.SetData(None)
                time.sleep(0.01)
            print('end cycle position')
            socket_hole.set_socket_pickup(None)
        time.sleep(0.01)
if __name__ == '__main__':
    main()