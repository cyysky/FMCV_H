import os
import traceback
import cv2

barcode = None
results_path = None
images_path = None
log_datetime = None
results = None
result_frame = None

def write_log():
    if str(results_path) != '.':
        os.makedirs(results_path, exist_ok=True)
        results_file_path = results_path / "{}_{}.txt".format(barcode,log_datetime)
        
        with open(results_file_path, "w") as file_log:        
            for src_n, src in enumerate(results):     
                for step_n, step in enumerate(results[src_n]):
                    for roi_n, roi_result in enumerate(results[src_n][step_n]):
                        file_log.write("{}".format(barcode))
                        file_log.write(",")
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
                        file_log.write("{}".format(state))
                        file_log.write(",")
                        if roi_result.get("type") == "CNN":
                            file_log.write("{}".format(roi_result.get("result_class")))
                            file_log.write(",")
                            file_log.write("{}".format(roi_result.get("result_score")))
                        if roi_result.get("type") == "QR":
                            file_log.write("{}".format(roi_result.get("CODE")))
                        if roi_result.get("type") == "FIDUCIAL":
                            file_log.write("{},".format(roi_result.get("score")))
                            file_log.write("{},".format(roi_result.get("offset_x")))
                            file_log.write("{}".format(roi_result.get("offset_y")))
                        file_log.write("\n")
    
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
                                cv2.imwrite(str(images_path / "{}_{}_{}_{}.jpg".format(barcode,f"{src_n+1}'{step_n+1}'{roi_result.get('name')}",state,log_datetime)), roi_result.get('result_image'))
                        except:
                            traceback.print_exc()