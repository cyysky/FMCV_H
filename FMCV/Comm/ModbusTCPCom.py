from pyModbusTCP.client import ModbusClient
import threading
import traceback
import os
import time
from datetime import datetime,timedelta

class ModbusTCP():
    def __init__(self,start, callback):
        self.start = start
        self.callback = callback
        self.modbus_tcp = self.create_thread()  
        self.com = self.modbus_tcp.com        
        
    def create_thread(self):
        config = self.start.Config.config
        if config['CONTROL']['modbus_type'] == 'JAKA':
            com = ModbusTCPThreadJAKA(parent=self,host=config['CONTROL']['modbus_ip'],port=int(config['CONTROL']['modbus_port']))
        
        if config['CONTROL']['modbus_type'] == 'DOBOT':
            com = ModbusTCPThreadDOBOT(parent=self,host=config['CONTROL']['modbus_ip'],port=int(config['CONTROL']['modbus_port']))
                
        com.daemon=True
        
        if config['CONTROL']['modbus_ip'] != "NONE":
            com.start()
        return com
        
    def on_callback(self, thread, data):
        #print (thread, data)
        self.callback(thread,data)

class ModbusTCPThreadJAKA(threading.Thread):
    def __init__(self, parent=None, host="10.5.5.100", port=502):
        super(ModbusTCPThreadJAKA, self).__init__()
        self.parent = parent
        if host != "NONE":
            self.com = ModbusClient(host=host, port=port, unit_id=1, auto_open=True)
        self.flag_next = False
        self.flag_stop = False
        
    def close(self):
        try:
            self.com.close()
        except:
            traceback.print_exc()
            
    def run(self):
        wait_time = 0.025
        self.last_state = False
        while True: 
            try:                   
                regs = self.com.read_discrete_inputs(8, 1)
                if regs:
                    if regs[0] != self.last_state:
                        self.last_state = regs[0]
                        if regs[0]:
                            print("trigged")
                            self.parent.on_callback(self, "T")
                else:
                    print("read error")
                if self.flag_next:    
                    time.sleep(wait_time)
                    self.com.write_single_coil(40,1)
                    self.flag_next = False
                    self.flag_stop = True
                if self.flag_stop:
                    time.sleep(wait_time)
                    self.com.write_single_coil(40,0)
                    self.flag_stop = False
            except:
                print("Modbus Thread Run Exception")
                traceback.print_exc() 
                time.sleep(1)
            time.sleep(wait_time)
    
            
    def go_next(self):
        self.flag_next = True

    def stop(self):   
        self.flag_stop = True
            
class ModbusTCPThreadDOBOT(threading.Thread):
    def __init__(self, parent=None, host="192.168.1.6", port=502):
        super(ModbusTCPThreadDOBOT, self).__init__()
        self.parent = parent
        if host != "NONE":
            self.com = ModbusClient(host=host, port=port, unit_id=1, auto_open=True)
    
    def close(self):
        try:
            self.com.close()
        except:
            traceback.print_exc()
            
    def run(self):        
        while True: 
            try:             
                regs = self.com.read_holding_registers(10, 1)
                if regs:
                    #print(regs[0])
                    if regs[0] == 1:
                        self.com.write_single_register(10,0)
                        print("Dobot RESET")
                        self.parent.on_callback(self, "RESET")                       
                else:
                    print("read error")
                
                regs = self.com.read_holding_registers(1, 1)
                if regs:
                    #print(regs[0])
                    if regs[0] == 1:
                        self.com.write_single_register(1,0)
                        print("trigged")
                        self.parent.on_callback(self, "T")                       
                else:
                    print("read error")
                    
            except:
                print("Modbus Thread Run Exception")
                traceback.print_exc() 
                time.sleep(1)
            time.sleep(0.1)
            
    def go_next(self):
        try:
            self.com.write_single_register(1,0)
            self.com.write_single_register(2,1)
            regs = self.com.read_holding_registers(1, 1)
            print(regs[0])
            regs = self.com.read_holding_registers(2, 1)
            print(regs[0])
            print("Modbus Dobot Go Next")
        except:
            print("Modbus Thread Run Exception")
            traceback.print_exc()
            
    def stop(self):
        pass
        
if __name__ == '__main__' :
    # import time
    # def callback(t,c):
        # print(f'{t},{c}')
    # manager(callback)
    # while True:
        # time.sleep(0.1)
    pass