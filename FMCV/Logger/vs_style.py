import os
import traceback
import cv2
from datetime import datetime, timedelta

barcode = None
results_path = None
images_path = None
log_datetime = None
results = None
result_frame = None

def init(start):
    global s
    global barcode, results_path, images_path, log_datetime, results, result_frame
    
    s = start
    
    barcode = s.Log.barcode
    results_path = s.Log.results_path
    images_path = s.Log.images_path
    log_datetime = s.Log.log_datetime
    results = s.Log.results
    result_frame = s.Log.result_frame

def write_log():
    global barcode, results_path, images_path, log_datetime, results, result_frame

    if str(results_path) != '.':
        os.makedirs(results_path, exist_ok=True)
        current_datetime = datetime.utcnow() + timedelta(hours=+8)
        
        results_file_path = results_path / "{}_{}.dat".format(barcode, current_datetime.strftime("%Y%m%d_%H%M%S"))
        
        with open(results_file_path, "w") as file_log:
            counter = 1
            file_log.write("V{}={}|".format(counter, barcode))
            
            counter+= 1
            file_log.write("V{}={}|".format(counter, "PASS" if s.Main.is_overall_pass() else "FAIL"))
        
            for src_n, src in enumerate(results):     
                for step_n, step in enumerate(results[src_n]):
                    for roi_n, roi_result in enumerate(results[src_n][step_n]):                    
                        counter+= 1
                        
                        file_log.write("V{}={}|".format(counter,src_n+1))
                        counter+= 1
                        file_log.write("V{}={}|".format(counter,step_n+1))
                        counter+= 1
                        file_log.write("V{}={}|".format(counter,roi_result["name"]))
                        counter+= 1
                        file_log.write("V{}={}|".format(counter,roi_result.get("type")))
                        counter+= 1
                        if roi_result.get("PASS"):
                            state = "PASS"
                        else:
                            state = "FAIL"
                        file_log.write("V{}={}|".format(counter,state))
                        counter+= 1
                        if roi_result.get("type") == "CNN":
                            file_log.write("V{}={}|".format(counter,roi_result.get("result_class")))
                            counter+= 1
                            file_log.write("V{}={:0.5f}|".format(counter,roi_result.get("result_score")))
                        if roi_result.get("type") == "QR":
                            file_log.write("V{}={}|".format(counter,roi_result.get("CODE")))
            
            log_date = current_datetime.strftime("%d/%m/%Y") #https://www.w3schools.com/python/python_datetime.asp
            log_time = current_datetime.strftime("%H:%M:%S") #https://www.w3schools.com/python/python_datetime.asp
            file_log.write("DAT={}|ZEI={}".format(log_date,log_time))

    
    if str(images_path) != '.':
        os.makedirs(images_path, exist_ok=True)
        for src_n, src in enumerate(results):     
                for step_n, step in enumerate(results[src_n]):
                    for roi_n, roi_result in enumerate(results[src_n][step_n]):    
                        if roi_result.get("PASS"):
                            state = "PASS"
                        else:
                            state = "FAIL"
                        try:
                            if str(images_path) != '.':
                                cv2.imwrite(str(images_path / "{}_{}_{}_{}.png".format(barcode,f"{src_n+1}'{step_n+1}'{roi_result.get('name')}",state,log_datetime)), roi_result.get('result_image'))
                        except:
                            traceback.print_exc()