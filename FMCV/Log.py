import traceback
import os
from datetime import datetime,timedelta
import cv2
from FMCV.Logger import flex_style, default_style, vs_style, kaifa_style

def init(s):
    global self
    self = s

def write_log():
    global barcode, results_path, images_path, log_datetime, results, result_frame
    
    global mes_path

    global self
    s = self
    
    print("Writing_log")
    
    try:
        
        barcode = s.Main.barcode
        results_path = s.Config.results_path
        images_path = s.Config.images_path
        mes_path = s.Config.mes_path
        log_datetime = datetime.utcnow() + timedelta(hours=+8)
        log_datetime = log_datetime.strftime("%Y%m%d_%H%M%S") #https://www.w3schools.com/python/python_datetime.asp
        results = s.Main.results
        result_frame = s.Main.result_frame
        
        if s.Config.log_type == "NORMAL":            
            default_style.barcode = barcode
            default_style.results_path = results_path
            default_style.images_path = images_path
            default_style.log_datetime = log_datetime
            default_style.results = results
            default_style.result_frame = result_frame
            default_style.write_log()
            
        if s.Config.log_type == "FLEX":
            flex_style.init(s)
            flex_style.write_log()
            
        if s.Config.log_type == "VS":
            vs_style.init(s)
            vs_style.write_log()
            
        if s.Config.log_type == "KAIFA":
            kaifa_style.init(s)
            kaifa_style.write_log()
            
        #update_total()
        
        self.Config.write_total()
        
    except:
        traceback.print_exc()
        
        
