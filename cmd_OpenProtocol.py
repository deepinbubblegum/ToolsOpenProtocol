class cmd_OpenProtocol:
    # 0001:Communication start
    def Communication_start(self):
        strHeader = '0001002000000000'
        strData = ''
        strAns = "00000000" + str(len(strHeader) + 4)
        strAns = strAns[-4:len(strAns)]
        strAns += (strHeader + '\0')
        return strAns

    # 0003:Communication stop
    def Communication_stop(self):
        strHeader = '0003001000000000'
        strData = ''
        strAns = "00000000" + str(len(strHeader) + 4)
        strAns = strAns[-4:len(strAns)]
        strAns += (strHeader + '\0')
        return strAns
    
    # 0010:Application ID upload request
    def Application_ID_upload_request(self):
        strHeader = '0010001000000000'
        strData = ''
        strAns = "00000000" + str(len(strHeader) + 4)
        strAns = strAns[-4:len(strAns)]
        strAns += (strHeader + '\0')
        return strAns

    # 0014:Application selected subscribe
    def Application_selected_subscribe(self):
        strHeader = '0014001000000000'
        strData = ''
        strAns = "00000000" + str(len(strHeader) + 4)
        strAns = strAns[-4:len(strAns)]
        strAns += (strHeader + '\0')
        return strAns

    # 0016:Application selected acknowledge
    def Application_selected_acknowledge(self):
        strHeader = '0016001000000000'
        strData = ''
        strAns = "00000000" + str(len(strHeader) + 4)
        strAns = strAns[-4:len(strAns)]
        strAns += (strHeader + '\0')
        return strAns

    # 0018:Select Application
    def Select_Application(self, strAppNo):
        strHeader = '0018001000000000'
        strData = strAppNo
        strHeader += strData
        strAns = "00000000" + str(len(strHeader) + 4)
        strAns = strAns[-4:len(strAns)]
        strAns += (strHeader + '\0')
        return strAns

    # 0034:Linking Group info subscribe
    def Linking_Group_info_subscribe(self):
        strHeader = '0034001000000000'
        strData = ''
        strAns = "00000000" + str(len(strHeader) + 4)
        strAns = strAns[-4:len(strAns)]
        strAns += (strHeader + '\0')
        return strAns

    # 0036:Linking Group info acknowledge
    def Linking_Group_info_acknowledge(self):
        strHeader = '0036001000000000'
        strData = ''
        strAns = "00000000" + str(len(strHeader) + 4)
        strAns = strAns[-4:len(strAns)]
        strAns += (strHeader + '\0')
        return strAns

    # 0042:Disable tool
    def Disable_tool(self):
        strHeader = '0042001000000000'
        strData = ''
        strAns = "00000000" + str(len(strHeader) + 4)
        strAns = strAns[-4:len(strAns)]
        strAns += (strHeader + '\0')
        return strAns

    # 0043:Enable tool
    def Enable_tool(self):
        strHeader = '0043001000000000'
        strData = ''
        strAns = "00000000" + str(len(strHeader) + 4)
        strAns = strAns[-4:len(strAns)]
        strAns += (strHeader + '\0')
        return strAns

    # 0051:Vehicle Id Number upload subscribe
    def Vehicle_Id_Number_upload_subscribe(self):
        strHeader = '0051001000000000'
        strData = ''
        strAns = "00000000" + str(len(strHeader) + 4)
        strAns = strAns[-4:len(strAns)]
        strAns += (strHeader + '\0')
        return strAns

    # 0053:Vehicle Id Number upload acknowledge
    def Vehicle_Id_Number_upload_acknowledge(self):
        strHeader = '0053001000000000'
        strData = ''
        strAns = "00000000" + str(len(strHeader) + 4)
        strAns = strAns[-4:len(strAns)]
        strAns += (strHeader + '\0')
        return strAns

    # 0060:Last tightening result data subscribe
    def Last_tightening_result_data_subscribe(self):
        strHeader = '0060001000000000'
        strData = ''
        strAns = "00000000" + str(len(strHeader) + 4)
        strAns = strAns[-4:len(strAns)]
        strAns += (strHeader + '\0')
        return strAns

    # 0062:Last tightening result data acknowledge
    def Last_tightening_result_data_acknowledge(self):
        strHeader = '0062001000000000'
        strData = ''
        strAns = "00000000" + str(len(strHeader) + 4)
        strAns = strAns[-4:len(strAns)]
        strAns += (strHeader + '\0')
        return strAns

    # 0080:Time upload request
    def Time_upload_request(self):
        strHeader = '0080001000000000'
        strData = ''
        strAns = "00000000" + str(len(strHeader) + 4)
        strAns = strAns[-4:len(strAns)]
        strAns += (strHeader + '\0')
        return strAns

    # 0130:Linking Group Off
    def Linking_Group_Off(self):
        strHeader = '0130001000000000'
        strData = ''
        strAns = "00000000" + str(len(strHeader) + 4)
        strAns = strAns[-4:len(strAns)]
        strAns += (strHeader + '\0')
        return strAns