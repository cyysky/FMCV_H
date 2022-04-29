import traceback
import configparser
import os
from pathlib import Path
import json

def init(s):
    global self
    self = s 

def print_config():
    global config , trigger_type , modbus_type , comport , profile , mode_name , non_stop
    global ai_minimum, train_rotate, train_brightness
    global reset_log, images_path , results_path , log_type
    
    comport = config['CONTROL']['comport']
    modbus_ip = config['CONTROL']['modbus_ip']
    modbus_port = config['CONTROL']['modbus_port']
    modbus_type = config['CONTROL']['modbus_type']
    r = config['LIGHTING']['red']
    g = config['LIGHTING']['green']
    b = config['LIGHTING']['blue']
    ai_minimum = float(config['AI']['minimum'])
    trigger_type = config['VISION']['trigger_type']
    camera_name = config['CAMERA']['name']
    cuda_visible_devices = config["CUDA"]["CUDA_VISIBLE_DEVICES"]
    profile = config['PROFILE']['name']
    mode_name = config['MODE']['name']
    non_stop = config['MODE']['non_stop']
    images_path = Path(config['LOG']['images_path'])
    results_path = Path(config['LOG']['results_path'])
    train_rotate = config['AI']['train_rotate']
    train_brightness = config['AI']['train_brightness']
    log_type = config['LOG']['type']
    reset_log = config['LOG']['reset_log']
    
    
    print(f'Mode Name: {mode_name}')
    print(f'Robot Non Stop: {non_stop}')
    print(f'Log type = {log_type}')
    print(f'Images Log Path: {images_path}')
    print(f'results_path Log Path: {results_path}')
    print(f'reset_log write log while reset step: {reset_log}')
    print(f'Profile: {profile}')
    print(f'comport: {comport}')
    print(f'modbus_ip: {modbus_ip}')
    print(f'modbus_port: {modbus_port}')
    print(f'red: {r}')
    print(f'green: {g}')
    print(f'blue: {b}')
    print(f'AI Minimum: {ai_minimum}')
    print(f'AI train_rotate: {train_rotate}')
    print(f'AI train_brightness: {train_brightness}')
    print(f'Trigger Type : {trigger_type}')
    print(f'Modbus Type : {modbus_type}')
    print(f'Camera Name : {camera_name}')
    print(f'cuda_visible_devices : {cuda_visible_devices}')
    
    
def write_config():
    global config
    try:    
        with open('config.ini', 'w') as configfile:
            print('Writing config.ini')
            config.write(configfile)
            return True
    except:
        traceback.print_exc()
    return False

try:
    config = configparser.ConfigParser()
    config.read('config.ini')

    print_config()
    
except:
    traceback.print_exc()
    
    config = configparser.ConfigParser()
    
    config.add_section('PROFILE')
    config['PROFILE']['name'] = 'default'

    config.add_section('CONTROL')

    config['CONTROL']['comport'] = 'NONE'
    config['CONTROL']['modbus_ip'] = 'NONE'
    config['CONTROL']['modbus_port'] = '502'
    config['CONTROL']['modbus_type'] = 'NONE'
    
    config.add_section('LIGHTING')
    
    config['LIGHTING']['red'] = "127"
    config['LIGHTING']['green'] = "127"
    config['LIGHTING']['blue'] = "127"
    
    config.add_section('CUDA')
    config["CUDA"]["CUDA_VISIBLE_DEVICES"] = "-1"
    
    config.add_section('AI')
    
    config['AI']['minimum'] = "0.6"
    config['AI']['train_rotate'] = "N"
    config['AI']['train_brightness'] = "N"
    config.add_section('VISION')
    
    config['VISION']['trigger_type'] = "NORMAL"
    
    config.add_section('CAMERA')
    
    config['CAMERA']['name'] = "Camera"
    
    config.add_section('MODE')
    
    config['MODE']['name'] = "ENGINEER"
    config['MODE']['non_stop'] = "Y"
    
    config.add_section('LOG')    
    config['LOG']['type'] = "NORMAL"
    config['LOG']['images_path'] = "LOG/IMAGES"
    config['LOG']['results_path'] = "LOG/RESULTS"
    config['LOG']['reset_log'] = "N"  #write log while reset
      
    write_config()
    
    print_config()
    

class_total = {"PASS":0,"FAIL":0}

try:
    with open(os.path.join("Profile",profile,'class_total.json')) as json_file:
        class_total = json.load(json_file)
except:
    traceback.print_exc()
    with open(os.path.join("Profile",profile,'class_total.json'), 'w') as fp:
        json.dump(class_total, fp, sort_keys=True, indent=4)
        
def write_total():
    with open(os.path.join("Profile",profile,'class_total.json'), 'w') as fp:
        json.dump(class_total, fp, sort_keys=True, indent=4)