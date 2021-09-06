import socket
import threading
import time
from datetime import datetime
from collections import deque 
from opensystem.cmd_OpenProtocol import cmd_OpenProtocol
from opensystem.data_info import Data_info

class OpenProtocol:
    def __init__(self, host, port):
        self.server = host
        self.port = port
        self.dataInfo = Data_info()
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.server, self.port))

        print('Intitialize network socket connected.')
        
        self.cmd = cmd_OpenProtocol()
        self.send_msg(self.cmd.Communication_stop())
        time.sleep(0.5)
        self.send_msg(self.cmd.Communication_start())
        
        print('Clear socket pipe line.')

        self.isClose = False
        self.t_recvMsg = threading.Thread(target=self.recv_msg)
        self.t_recvMsg.daemon = True
        self.t_recvMsg.start()

        print('Created Threading recive pcakage.')
        
        self.Data = {}
        # self.Data_old = {}
        
        # parameter and flag
        self.online = False

        self.isLock_at_batch_accepted = False
        self.deque = deque(maxlen=1)
        print('Initialize valable begin')

    def recv_filter(self, recv_msg):
        recv_msg = recv_msg.decode('ascii')
        # recv_msg = recv_msg.split(" ")
        # array_list = list(filter(None, recv_msg))
        # print(array_list)
        return recv_msg

    def reconnect_pipe(self):
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((self.server, self.port))
            self.send_msg(self.cmd.Communication_stop())
            time.sleep(0.2)
            self.send_msg(self.cmd.Communication_start())
            time.sleep(0.2)
        except ArithmeticError:
            time.sleep(1)

    def send_msg(self, send_msg):
        try:
            time.sleep(0.01)
            send_msg = send_msg.encode('ascii')
            self.conn.sendall(send_msg)
            return True
        except Exception as err:
            self.close()
            self.reconnect_pipe()
            return False
        
    def res_result_data_acknowledge(self):
        self.Last_result_data_subscribe = True
        self.send_msg(self.cmd.Last_tightening_result_data_acknowledge())
    
    def res_Vehicle_Id_Number_upload_acknowledge(self):
        self.VIN_upload_subscribe = True
        self.send_msg(self.cmd.Vehicle_Id_Number_upload_acknowledge())
        
    def res_Linking_Group_info_acknowledge(self):
        self.Linking_Group_info_acknowledge = True
        self.send_msg(self.cmd.Linking_Group_info_acknowledge())

    def msg_operation(self, msg):
        recv_mid = msg[4:8]
        if recv_mid == '0002': # Communication start acknowledge
            # example recv 006200020020        010000020503                         04ATG
            self.Rev_num_msg = msg[8:11]
            self.No_ack_flag = msg[11:12]
            self.Cell_id = msg[22:26]
            self.Channel_id = msg[28:30]
            self.Controller_Name = msg[32:57]
            self.Supplier_code = msg[59:62]
            self.online = True
        elif recv_mid == '0081':
            # example recv 003900810010        2021-09-01:15:01:10
            self.Rev_num_msg = msg[8:11]
            self.No_ack_flag = msg[11:12]
            self.Time_msg = datetime.strptime(msg[20:39], '%Y-%m-%d:%H:%M:%S')
        elif recv_mid == '0005': #Command accepted
            msg_accepted = msg[20:24]
            if msg_accepted == '0043': # Enable Tools CMD accepted
            # example recv 002400050010        0043
                self.Enable_tools = True
                self.Rev_num_msg = msg[8:11]
                self.No_ack_flag = msg[11:12]
            elif msg_accepted == '0042':
                self.Enable_tools = False
                self.Rev_num_msg = msg[8:11]
                self.No_ack_flag = msg[11:12]
            elif msg_accepted == '0051': #Vehicle Id Number upload subscribe CMD accepted
                # 002400050010        0051
                self.VIN_upload_subscribe = True
                self.Rev_num_msg = msg[8:11]
                self.No_ack_flag = msg[11:12]
                
            elif msg_accepted == '0060': # Last tightening result data subscribe CMD accepted
            # example recv 002400050010        0060
                self.Last_result_data_subscribe = True
                self.Rev_num_msg = msg[8:11]
                self.No_ack_flag = msg[11:12]
            elif msg_accepted:
                print('msg_accepted : ', msg)
                
        elif recv_mid == '0004': #Command error
            msg_not_accept = msg[20:24]
            # example recv 002600040010        000196
            if msg_not_accept == '0001': # Communication error
                self.online = False
                self.Rev_num_msg = msg[8:11]
                self.No_ack_flag = msg[11:12]
                
            elif msg_not_accept == '0051':
                self.VIN_upload_subscribe = False
                self.Rev_num_msg = msg[8:11]
                self.No_ack_flag = msg[11:12]
                
            elif msg_not_accept == '0060': # Last tightening result data subscribe CMD not accepted
            # example recv 002600040010        006009
                self.Last_result_data_subscribe = False
                self.Rev_num_msg = msg[8:11]
                self.No_ack_flag = msg[11:12]
            
            elif msg_not_accept == '0034':
                self.Linking_Group_info_acknowledge = False
                self.Rev_num_msg = msg[8:11]
                self.No_ack_flag = msg[11:12]
            
            elif msg_not_accept:
                print('msg_not_accepted : ', msg)
                self.Rev_num_msg = msg[8:11]
                self.No_ack_flag = msg[11:12]
        
        elif recv_mid == '0052':
            self.Rev_num_msg = msg[8:11]
            self.No_ack_flag = msg[11:12]
            self.VIN_Number_CODE = msg[20:45]
            # select Enter ID CODE
            # print(self.VIN_Number_CODE)
            self.res_Vehicle_Id_Number_upload_acknowledge()
            
        elif recv_mid == '0061':
            # example recv 023100610010        010000020503                         041234                     050106002070005080001091101111120000001300130014000000150000001600010170037018003601900361202021-09-01:16:00:42212021-08-31:18:00:54220230000000266
            self.Rev_num_msg = msg[8:11]
            self.No_ack_flag = msg[11:12]
            self.Cell_id = msg[22:26]
            self.Channel_id = msg[28:30]
            self.Controller_Name = msg[32:57]
            self.VIN_Number = msg[59:84]
            self.Linking_Group_ID = msg[86:88]
            self.Application_ID = msg[90:93]
            self.Batch_size = msg[95:99]
            self.Batch_counter = msg[101:105]
            self.Tightening_Status = msg[107:108] #The tightening status is one byte long and specified by one ASCII digit. 0=tightening NOK, 1=tightening OK.
            self.Torque_status = msg[110:111] #0=Low, 1=OK, 2=High
            self.Angle_status = msg[113:114] #0=Low, 1=OK, 2=High
            self.Torque_Min_limit = msg[116:122]
            self.Torque_Max_limit = msg[124:130]
            self.Torque_final_targe = msg[132:138]
            self.Torque = msg[140:146]
            self.Angle_Min = msg[148:153]
            self.Angle_Max = msg[155:160]
            self.Final_Angle_Target = msg[162:167]
            self.Angle = msg[169:174]
            self.Time_stamp = datetime.strptime(msg[176:195], '%Y-%m-%d:%H:%M:%S')
            self.Date_time_last_change_App_settings = datetime.strptime(msg[197:216], '%Y-%m-%d:%H:%M:%S')
            self.Batch_status = msg[218:219] #0=batch NOK (batch notcompleted), 1=batch OK, 2=batch not used.
            self.Tightening_ID = msg[221:231]
            self.Data = {
                'Rev_num_msg': self.Rev_num_msg, 'No_ack_flag' : self.No_ack_flag, 'Cell_id': self.Cell_id,
                'Channel_id' : self.Channel_id, 'Controller_Name': self.Controller_Name, 'VIN_Number': self.VIN_Number,
                'Linking_Group_ID' : self.Linking_Group_ID, 'Application_ID' : self.Application_ID, 'Batch_size' : self.Batch_size,
                'Batch_counter' : self.Batch_counter, 'Tightening_Status' : self.Tightening_Status, 'Torque_status': self.Torque_status,
                'Angle_status' : self.Angle_status, 'Torque_Min_limit' : self.Torque_Min_limit, 'Torque_Max_limit' : self.Torque_Max_limit,
                'Torque_final_targe' : self.Torque_final_targe, 'Torque' : self.Torque, 'Angle_Min' : self.Angle_Min, 'Angle_Max' : self.Angle_Max,
                'Final_Angle_Target' : self.Final_Angle_Target, 'Angle' : self.Angle, 'Time_stamp' : self.Time_stamp, 'Date_time_last_change_App_settings' : self.Date_time_last_change_App_settings,
                'Batch_status' : self.Batch_status, 'Tightening_ID' : self.Tightening_ID
            }
            self.res_result_data_acknowledge()
            # print(self.Data)
            
        elif recv_mid == '0035':
            self.Rev_num_msg = msg[8:11]
            self.No_ack_flag = msg[11:12]
            print(msg)
            self.res_Linking_Group_info_acknowledge()
        
        elif recv_mid == '0011':
        # 002900110010        002001002
            self.Rev_num_msg = msg[8:11]
            self.No_ack_flag = msg[11:12]
            self.Number_of_valid_Application = msg[20:23]
            self.Application_numbers_of_the_torque_controller = msg[23: 23 + (3 * int(self.Number_of_valid_Application))]
        elif recv_mid:
            print(msg)
      
    def GetData(self):
        return self.Data
      
    def recv_msg(self):
        while self.isClose is not True:
            try:
                recv_msg = self.conn.recv(1024)
                if recv_msg:
                    recv_msg = self.recv_filter(recv_msg)
                    thread = threading.Thread(target=self.msg_operation, args=(recv_msg,))
                    thread.daemon = True
                    thread.start()
            except Exception as e:
                pass
            time.sleep(0.001)
            
    def get_recv(self):
        if self.deque:
            Recv = self.deque[-1]
            self.recv_msg_data = Recv
        return Recv

    def close(self):
        self.isClose = True
        self.conn.close()
