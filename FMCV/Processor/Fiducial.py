import cv2
import traceback
import copy 



def process_fiducial(start, result, frm, src_n, step_n, roi_n):

    h,w = frm.shape[:2]
    roi = result
    
    m = roi['margin']
    
    x1 = roi['x1'] - m
    y1 = roi['y1'] - m
    x2 = roi['x2'] + m
    y2 = roi['y2'] + m
    
    if x1 < 0 : x1 = 0 
    if y1 < 0 : y1 = 0 
    if x2 > w : x2 = w 
    if y2 > h : y2 = h
    
    cropped = frm[y1:y2,x1:x2]
   
    res,top_left,bottom_right,top_val,cropped = start.Cv.match_template(roi['img'],frm[y1:y2,x1:x2])
    
    result.update({'result_image':copy.deepcopy(cropped)})
    
    if roi.get('minimal') <= top_val:
        result.update({"PASS":True})
    else:
        result.update({"PASS":False})
        
    result.update({'result_image':copy.deepcopy(cropped)})
    result.update({'score':top_val})
    result.update({'offset_x':top_left[0]-m})
    result.update({'offset_y':top_left[1]-m})
    
    print('{} {} {} {} {} {}'.format(m,x1,y1,top_left,top_val,roi.get('minimal') <= top_val,roi.get('minimal')))
    
    offset = {}
    offset.update({ "x":result.get("offset_x") , "y":result.get("offset_y")})
    
    start.Com.update_offset(offset)
    
    return result