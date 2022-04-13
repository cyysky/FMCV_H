import cv2
import numpy as np

def _show_im(frm):
    cv2.namedWindow("a", cv2.WINDOW_NORMAL)
    cv2.imshow("a",frm)        
    cv2.waitKey(0)

def to_gray(CurrentImage):
    # Convert to grayscale. 
    if len(CurrentImage.shape)==3:
        img1 = cv2.cvtColor(CurrentImage, cv2.COLOR_BGR2GRAY) 
    else:
        img1 = CurrentImage
    return img1 
    
def to_color(CurrentImage):
    # Convert to grayscale. 
    if len(CurrentImage.shape)<3:
        img1 = cv2.cvtColor(CurrentImage, cv2.COLOR_GRAY2BGR)
    else:
        img1 = CurrentImage
    return img1

def match_template(TemplateImage,CurrentImage):
    #Reference https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html
    #Get width and height
    w = TemplateImage.shape[1]
    h = TemplateImage.shape[0]
    
    selected = 2 - 1
    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    method = eval(methods[selected])
    
    # Template matching
    res = cv2.matchTemplate(to_gray(CurrentImage),to_gray(TemplateImage),method)
    
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)    
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
        top_val = min_val
    else:
        top_left = max_loc
        top_val = max_val
    bottom_right = (top_left[0] + w, top_left[1] + h)
    loc = np.where(res>=0.6)

    croppedImage = CurrentImage[top_left[1]:bottom_right[1],top_left[0]:bottom_right[0]].copy()

    #cv2.putText(croppedImage,str(top_val),(-10,11),cv2.FONT_HERSHEY_SIMPLEX,0.33,(0,0,255),1)

    return res,top_left,bottom_right,top_val,croppedImage  