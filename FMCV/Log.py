import traceback
import os
from datetime import datetime,timedelta
import cv2
from FMCV.Logger import flex_style, default_style, vs_style

def init(s):
    global self
    self = s

def write_log():
    global barcode, results_path, images_path, log_datetime, results, result_frame

    global self
    s = self
    
    print("Writing_log")
    
    try:
        
        barcode = s.Main.barcode
        results_path = s.Config.results_path
        images_path = s.Config.images_path
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
            flex_style.barcode = barcode
            flex_style.results_path = results_path
            flex_style.images_path = images_path
            flex_style.log_datetime = log_datetime
            flex_style.results = results
            flex_style.result_frame = result_frame
            flex_style.write_log()
            
        if s.Config.log_type == "VS":
            vs_style.init(s)
            vs_style.write_log()
            
        update_total()
        
        self.Config.write_total()
        
    except:
        traceback.print_exc()
        
        
def update_total():
    # is_pass = True
    # for src_n, src in enumerate(self.Main.results):
        # for step_n, step in enumerate(self.Main.results[src_n]):
            # for roi_n, roi in enumerate(self.Main.results[src_n][step_n]):
                # if roi.get('PASS'):
                    # is_pass = True
                # else :
                    # is_pass = False
    
    
    
    total_pass = self.Config.class_total.get("PASS")
    total_fail = self.Config.class_total.get("FAIL")
    
    if self.Main.is_overall_pass():
        total_pass = total_pass + 1
    else :
        total_fail = total_fail + 1
    self.Config.class_total.update({"PASS":total_pass,"FAIL":total_fail})