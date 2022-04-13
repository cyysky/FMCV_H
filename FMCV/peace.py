#https://stackoverflow.com/questions/110362/how-can-i-find-the-current-os-in-python
import platform
import os
import sys

#from hashlib import blake2b
import hashlib

import subprocess
from subprocess import Popen, PIPE

import traceback

import re


def peace():
    global uniqueId
    try:
        #print("peace")
        platformName = platform.system()
        #print(platformName)
        if platformName == "Linux":   

            if platform.linux_distribution()[0]=='Ubuntu':
                userHash = sha(getsda())
            else:
                GetMAC('wlan0')
                GetMAC('eth0')       
                getserial()      
                
                h = sha(gen())
                userHash = sha(gen())  # User's hash

            if VisionIC(userHash):
                return
            
        elif platformName =="Windows":   
            h = winhdd()+wincpu()
            h = sha(h)
            userHash = sha(h) # User's hash      

            if VisionIC(userHash):
                return
      
        raise Exception 
    except:
        # https://stackoverflow.com/questions/9555133/e-printstacktrace-equivalent-in-python
        #traceback.print_exc()
        # https://stackoverflow.com/questions/73663/terminating-a-python-script
        os._exit(0)
        sys.exit(0)
        raise SystemExit  
        1/0      
        pass
            
  
def Peace(message):
    try:
        sys.stdout.write(".")
        sys.stdout.flush()
        return sha(message+message)
    except:
        # https://stackoverflow.com/questions/9555133/e-printstacktrace-equivalent-in-python
        #traceback.print_exc()
        # https://stackoverflow.com/questions/73663/terminating-a-python-script
        os._exit(0)
        sys.exit(0)
        raise SystemExit  
        1/0      
        pass
            
     
def Vision(inputUniqueId):
    global uniqueId
    try:
        h = sha(uniqueId+uniqueId+uniqueId) # License
        if h == license()['Vision']:
            return True # print("OK")
        print("--------------------------------------------------------------------------------")
        print("#                Please contact reseller for valid license                     #")
        print("--------------------------------------------------------------------------------")
        print("|                                                                              |")
        print("|       "+uniqueId+"       |") 
        print("|                                                                              |")
        print("--------------------------------------------------------------------------------")      
        raise Exception 
    except:
        # https://stackoverflow.com/questions/9555133/e-printstacktrace-equivalent-in-python
        #traceback.print_exc()
        # https://stackoverflow.com/questions/73663/terminating-a-python-script
        os._exit(0)
        sys.exit(0)
        #quit()
        raise SystemExit  
        1/0      
        pass  
        

def VisionIC(uniqueId):
    try:
        h = sha(uniqueId+uniqueId) # License
        if h == license()['VisionIC']:
            return True # print("OK")
        print("--------------------------------------------------------------------------------")
        print("#                Please contact reseller for valid license                     #")
        print("--------------------------------------------------------------------------------")
        print("|                                                                              |")
        print("|       "+uniqueId+"       |") 
        print("|                                                                              |")
        print("--------------------------------------------------------------------------------")      
        raise Exception 
    except:
        # https://stackoverflow.com/questions/9555133/e-printstacktrace-equivalent-in-python
        #traceback.print_exc()
        # https://stackoverflow.com/questions/73663/terminating-a-python-script
        os._exit(0)
        sys.exit(0)
        #quit()
        raise SystemExit  
        1/0      
        pass

def VisionCelsius(InputUniqueId):
    global uniqueId
    try:
        h = sha(uniqueId)
        h = sha(h) # License
        if h == license()['VisionCelsius']:
            return True # print("OK")
        print("--------------------------------------------------------------------------------")
        print("#                Please contact reseller for valid Celsius license             #")
        print("--------------------------------------------------------------------------------")
        print("|                                                                              |")
        print("|       "+uniqueId+"       |") 
        print("|                                                                              |")
        print("--------------------------------------------------------------------------------")      
        raise Exception 
    except:
        # https://stackoverflow.com/questions/9555133/e-printstacktrace-equivalent-in-python
        #traceback.print_exc()
        # https://stackoverflow.com/questions/73663/terminating-a-python-script
        os._exit(0)
        sys.exit(0)
        #quit()
        raise SystemExit  
        1/0      
        pass         
     
def license():
    try:
        # https://www.programiz.com/python-programming/methods/built-in/getattr
        # Reference pyinstaller path https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
        if getattr(sys, 'frozen', False):
            dirName = os.path.dirname(sys.executable)
        elif __file__:
            dirName = os.getcwd()
        #print(dirName)
        lic = { 'Vision':'Vision',
                'VisionIC':'VisionIC',
                'VisionCelsius':'VisionCelsius'}

        str = open(os.path.join(dirName,'License')).read()
        for l in str.split('\n'):
            if l.startswith('VisionIC:'):
                lic.update({'VisionIC':l[9:]})
            if l.startswith('Vision:'):
                lic.update({'Vision':l[7:]})
            if l.startswith('VisionCelsius:'):
                lic.update({'VisionCelsius':l[14:]})    
        #print(lic)        
        return lic
    except:
        print("")
        print("Unable to open License")
        print("")
        return {'Vision':'Vision','VisionIC':'VisionIC'}
        # https://stackoverflow.com/questions/9555133/e-printstacktrace-equivalent-in-python
        #traceback.print_exc()
        # https://stackoverflow.com/questions/73663/terminating-a-python-script
        #print("here is after return")
        os._exit(0)
        sys.exit(0)
        #quit()
        raise SystemExit  
        1/0      
        pass

# def encrypt(self,key,message):
    # try:
        # key = key.encode('utf-8')
        # message = message.encode('utf-8')
        # h = blake2b(key)
        # h.update(message)
        # return h.hexdigest()
    # except:
        # # https://stackoverflow.com/questions/73663/terminating-a-python-script
        # os._exit(0)
        # sys.exit(0)
        # #quit()
        # raise SystemExit  
        # 1/0
        # pass
        

def sha(message):
    try:    
        return hashlib.sha3_256(message.encode('utf-8')).hexdigest()
    except:
        # https://stackoverflow.com/questions/73663/terminating-a-python-script
        os._exit(0)
        sys.exit(0)
        #quit()
        raise SystemExit  
        1/0
        pass
        
# def compare(self,key,message):
    # try:
        # h = blake2b(key)
        # h.update(message)
        # return h.hexdigest()
    # except:
        # # https://stackoverflow.com/questions/73663/terminating-a-python-script
        # os._exit(0)
        # sys.exit(0)
        # #quit()
        # raise SystemExit  
        # 1/0
        # pass


def gen():
    try:
        # https://www.raspberrypi.org/documentation/hardware/raspberrypi/otpbits.md
        s = subprocess.check_output(["vcgencmd","otp_dump"]).decode('utf-8')
        #print(type(s))
        s = s.split('\n')
        for l in s:
            # https://www.daniweb.com/programming/software-development/threads/317757/print-lines-that-start-with-a-specific-word
            if l.startswith('29:'):
                #print (l)
                return l[3:11]
        raise Exception 
    except:
        # https://stackoverflow.com/questions/73663/terminating-a-python-script
        os._exit(0)
        sys.exit(0)
        #quit()
        raise SystemExit  
        1/0   
        pass
        
def winhdd():
# https://raspberrypi.stackexchange.com/questions/2086/how-do-i-get-the-serial-number
    # Extract serial from cpuinfo file
    try:
        #https://www.reddit.com/r/learnpython/comments/2zv7rg/subprocess_and_wmic_command/
        f =subprocess.check_output(['wmic','diskdrive','get','Name,SerialNumber']).decode("utf-8")
        for line in f.split('\n'): 
            #print(line)
            if line.startswith('\\\\.\\PHYSICALDRIVE0'):
                hdd = line[20:]
                #https://stackoverflow.com/questions/7147396/python-how-to-delete-hidden-signs-from-string
                hdd = re.sub("[^a-z0-9]+","", hdd, flags=re.IGNORECASE)
                #print(hdd)
                #print(len(hdd))
                
                return hdd
            #f.close()
        raise Exception
    except:
        # https://stackoverflow.com/questions/9555133/e-printstacktrace-equivalent-in-python
        #traceback.print_exc()
        # https://stackoverflow.com/questions/73663/terminating-a-python-script
        os._exit(0)
        sys.exit(0)
        #quit()
        raise SystemExit  
        1/0
        pass
        

def wincpu():
# https://raspberrypi.stackexchange.com/questions/2086/how-do-i-get-the-serial-number
    # Extract serial from cpuinfo file
    try:
        #https://www.reddit.com/r/learnpython/comments/2zv7rg/subprocess_and_wmic_command/
        f =subprocess.check_output(['wmic','cpu','list','full']).decode("utf-8")
        for line in f.split('\n'): 
            #print(line)
            if line.startswith('ProcessorId='):
                cpu = line[12:]
                #https://stackoverflow.com/questions/7147396/python-how-to-delete-hidden-signs-from-string
                cpu = re.sub("[^a-z0-9]+","", cpu, flags=re.IGNORECASE)
                #print(cpu)
                #print(len(cpu))
                return cpu
            #f.close()
        raise Exception
    except:
        # https://stackoverflow.com/questions/9555133/e-printstacktrace-equivalent-in-python
        #traceback.print_exc()
        # https://stackoverflow.com/questions/73663/terminating-a-python-script
        os._exit(0)
        sys.exit(0)
        #quit()
        raise SystemExit  
        1/0
        pass
           
def getsda():
    try:
        tem = open("/sys/class/thermal/thermal_zone0/temp").read()
        #tem = open('/proc/cpuinfo').read()
        #print(tem)
        #print(int(tem))
        tem = int(tem)

        # https://www.raspberrypi.org/documentation/hardware/raspberrypi/otpbits.md
        s = subprocess.check_output("lsblk --nodeps -no serial /dev/sda",shell=True).decode('utf-8')
        #print(type(s))
        s = re.sub("[^a-z0-9]+","", s, flags=re.IGNORECASE)
        #print("--{}--".format(s))        
        #print(len(s))
        if len(s)>5:
            return s

        #s = s.split('\n')
        #for l in s:
            # https://www.daniweb.com/programming/software-development/threads/317757/print-lines-that-start-with-a-specific-word
            #if l.startswith('29:'):
                #print (l)
                #return l[3:11]
        raise Exception 
    except:
        # https://stackoverflow.com/questions/73663/terminating-a-python-script
        os._exit(0)
        sys.exit(0)
        #quit()
        raise SystemExit  
        1/0   
        pass



def getserial():
# https://raspberrypi.stackexchange.com/questions/2086/how-do-i-get-the-serial-number
    # Extract serial from cpuinfo file
    try:
        f =open('/proc/cpuinfo').read()
        for line in f.split('\n'): 
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
                return cpuserial
            #f.close()
        raise Exception
    except:
        # https://stackoverflow.com/questions/9555133/e-printstacktrace-equivalent-in-python
        # traceback.print_exc()
        # https://stackoverflow.com/questions/73663/terminating-a-python-script
        os._exit(0)
        sys.exit(0)
        #quit()
        raise SystemExit  
        1/0
        pass
        
def GetMAC(interface='eth0'):#'wlan0'
# https://www.raspberrypi-spy.co.uk/2012/06/finding-the-mac-address-of-a-raspberry-pi/
# Return the MAC address of the specified interface
    try:
        # https://pyformat.info/
        #print('/sys/class/net/{0}/address'.format(interface))
        
        str = open('/sys/class/net/{0}/address'.format(interface)).read()
        return str[0:17]
    except:
        # https://stackoverflow.com/questions/73663/terminating-a-python-script
        os._exit(0)
        sys.exit(0)
        #quit()
        raise SystemExit  
        1/0
        pass
        
def Info(self):
    #https://archlinuxarm.org/forum/viewtopic.php?f=67&t=12577
    try:
        str = open('/sys/firmware/devicetree/base/serial-number').read()
        return str
    except:
        # https://stackoverflow.com/questions/73663/terminating-a-python-script
        os._exit(0)
        sys.exit(0)
        #quit()
        raise SystemExit  
        1/0
        pass
        
            
peace()
if __name__ == '__main__':
    peace()
    os._exit(0)
    sys.exit(0)
    raise SystemExit  
    1/0      
    pass
  
  