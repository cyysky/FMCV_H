# #==========================================================================
# import hashlib
# from FMCV.peace import Peace,license
# lic = license()['Vision']
# if (hashlib.sha3_256((lic+lic).encode('utf-8')).hexdigest()!=Peace(lic)):
    # # https://stackoverflow.com/questions/9555133/e-printstacktrace-equivalent-in-python
    # #traceback.print_exc()
    # # https://stackoverflow.com/questions/73663/terminating-a-python-script
    # import os
    # import sys
    # os._exit(0)
    # sys.exit(0)
    # raise SystemExit  
    # 1/0      
    # pass
# #==========================================================================

import cv2
import copy
import traceback

from FMCV.Processor import Barcode
from FMCV.Processor import Fiducial
    

def init(s):
    global start
    start = s 

def execute(frm, src_n,step_n,roi_n):
    h,w = frm.shape[:2]
    roi = start.Main.results[src_n][step_n][roi_n]
    result = roi
    
    if roi['type'] == "CNN":
        m = roi['margin']
        x1 = roi['x1'] - m
        y1 = roi['y1'] - m
        x2 = roi['x2'] + m
        y2 = roi['y2'] + m
        if m > 0:
            x1 = x1 - m
            y1 = y1 - m
            x2 = x2 + m
            y2 = y2 + m
            if x1 < 0 : x1 = 0 
            if y1 < 0 : y1 = 0 
            if x2 > w : x2 = w 
            if y2 > h : y2 = h

            res,top_left,bottom_right,top_val,cropped = start.Cv.match_template(roi['img'],frm[y1:y2,x1:x2])
        else:
            cropped = frm[y1:y2,x1:x2]
            
        resized = cv2.resize(cropped,(224,224))
        scaled_im = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        scaled_im = scaled_im * (1./255) 
        classify,score = start.CNN.predict("go",scaled_im)
        result_name = start.CNN.get_class_name(classify)
                
        if roi["class"] == result_name :
            if score < start.Config.ai_minimum:
                result.update({"PASS":False})
            else:
                result.update({"PASS":True})
        else:
            result.update({"PASS":False})
        
        result.update({'result_image':copy.deepcopy(cropped)})
        result.update({"result_class":result_name})
        result.update({"result_score":score})
        print(f'{roi["name"]} {result_name}:{score}')
        
    if roi['type'] == "QR":
        result = Barcode.process_barcode(start, result, frm, src_n, step_n, roi_n)
    
    if roi['type'] == "FIDUCIAL":
        result = Fiducial.process_fiducial(start, result, frm, src_n, step_n, roi_n)
        
    return result