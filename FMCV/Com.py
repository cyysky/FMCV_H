from FMCV.Comm import SerialCom, ModbusTCPCom, MESCom

import traceback
import time
import traceback

serial = None
modbusTCP = None
mes = None

def callback(obj, msg):
    global start
    msg = ''.join(filter(str.isalnum, msg)) 
    print(msg)
    if msg == "T":
        print("Callback Triggered")
        start.ActionUi.detect()
        #start.MainUi.view.after(1, start.ActionUi.detect)
    if msg == "RESET":
        print("Callback RESET")
        #start.MainUi.view.after(1, start.ActionUi.reset_detection_step)
        start.ActionUi.reset_detection_step()
    if msg == "VSMES":
        print("VS MES Callback Triggered")
        start.ActionUi.detect(SN=obj.barcode)

def init(in_start):
    global start, modbusTCP, serial, mes
    start = in_start
    if start.Config.modbus_type in ("JAKA","DOBOT"):
        try:
            modbusTCP = ModbusTCPCom.ModbusTCP(start,callback)
        except:
            traceback.print_exc()

    if start.Config.comport != "NONE":
        try:
            serial = SerialCom.Serial(start,callback)
            time.sleep(2)
            serial.write_lighting()
        except:
            traceback.print_exc()
    
    if start.Config.mes_connect_type != 'NONE':
        try:
            mes = MESCom.MES(start,callback)
        except:
            traceback.print_exc()
            
def go_next():
    global start, modbusTCP, serial
    
    if start.Config.comport != "NONE":        
        serial.write_result(bytes(f'1\n', 'utf8'))
        print("Serial Next")
    if start.Config.modbus_type in ("JAKA","DOBOT"):
        modbusTCP.modbus_tcp.go_next()   
        print("Modbus Next")
    
    
def failed():
    global start, modbusTCP, serial
    
    if start.Config.comport != "NONE":        
        serial.write_result(bytes(f'0\n', 'utf8'))
        print("Serial Fail Sent")
    if start.Config.modbus_type in ("JAKA","DOBOT"):
        modbusTCP.modbus_tcp.fail()   
        print("Modbus Fail Sent")
    
def alarm():
    failed()

def update_offset(offset):
    global start
    print("Comm offset")
    if offset.get("x") is not None and offset.get("y") is not None:
        if start.Config.modbus_type in ("JAKA"):
            print("update offset")
            x = offset.get("x")
            y = offset.get("y")
            modbusTCP.modbus_tcp.fiducial_offset(x,y)
    