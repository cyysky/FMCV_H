from FMCV.Comm import SerialCom, ModbusTCPCom

import traceback
import time
import traceback
serial = None
modbusTCP = None

def callback(obj, msg):
    global self
    msg = ''.join(filter(str.isalnum, msg)) 
    print(msg)
    if msg == "T":
        print("Callback Triggered")
        self.ActionUi.detect()
        #self.MainUi.view.after(1, self.ActionUi.detect)
    if msg == "RESET":
        print("Callback RESET")
        #self.MainUi.view.after(1, self.ActionUi.reset_detection_step)
        self.ActionUi.reset_detection_step()

def init(s):
    global self, modbusTCP, serial
    self = s
    if self.Config.modbus_type in ("JAKA","DOBOT"):
        try:
            modbusTCP = ModbusTCPCom.ModbusTCP(self,callback)
        except:
            traceback.print_exc()

    if self.Config.comport != "NONE":
        try:
            serial = SerialCom.Serial(self,callback)
            time.sleep(2)
            serial.write_lighting()
        except:
            traceback.print_exc()
    
def go_next():
    global self, modbusTCP, serial
    
    if self.Config.comport != "NONE":        
        serial.write_result(bytes(f'1\n', 'utf8'))
        print("Serial Next")
    if self.Config.modbus_type in ("JAKA","DOBOT"):
        modbusTCP.modbus_tcp.go_next()   
        print("Modbus Next")
    
    
def failed():
    global self, modbusTCP, serial
    
    if self.Config.comport != "NONE":        
        serial.write_result(bytes(f'0\n', 'utf8'))
        print("Serial Fail Sent")
    if self.Config.modbus_type in ("JAKA","DOBOT"):
        modbusTCP.modbus_tcp.fail()   
        print("Modbus Fail Sent")
    
def alarm():
    failed()

def update_offset(offset):
    print("Comm offset")
    if offset.get("x") is not None and offset.get("y") is not None:
        if self.Config.modbus_type in ("JAKA"):
            print("update offset")
            x = offset.get("x")
            y = offset.get("y")
            modbusTCP.modbus_tcp.fiducial_offset(x,y)
    