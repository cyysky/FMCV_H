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
        results_file_path = results_path / "{}_{}.csv".format(barcode,log_datetime)
        
        overall_result = True
        
        with open(results_file_path, "w") as file_log:    
            
            file_log.write("Camera,Step,ROI_Name,Type,Result,Aux1,Aux2,Aux3\n")   
            
            for src_n, src in enumerate(results):     
                for step_n, step in enumerate(results[src_n]):
                    for roi_n, roi_result in enumerate(results[src_n][step_n]):
                        #file_log.write("{}".format(barcode))
                        #file_log.write(",")
                        file_log.write("{}".format(src_n+1))
                        file_log.write(",")
                        file_log.write("{}".format(step_n+1))
                        file_log.write(",")
                        file_log.write("{}".format(roi_result["name"]))
                        file_log.write(",")
                        file_log.write("{}".format(roi_result.get("type")))
                        file_log.write(",")
                        if roi_result.get("PASS"):
                            state = "PASS"
                        else:
                            state = "FAIL"
                            overall_result = False                            
                        file_log.write("{}".format(state))
                        file_log.write(",")
                        if roi_result.get("type") == "CNN":
                            file_log.write("{}".format(roi_result.get("result_class")))
                            file_log.write(",")
                            file_log.write("{}".format(roi_result.get("result_score")))
                        if roi_result.get("type") == "QR":
                            file_log.write("{}".format(roi_result.get("CODE")))
                        file_log.write("\n")
            
            
            file_log.write(",,,RESULT,{},,,\n".format("PASS" if overall_result else "FAIL"))   
            
    
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
                            #traceback.print_exc()
                            pass