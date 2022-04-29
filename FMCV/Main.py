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
import json
import copy
import cv2
from PIL import Image, ImageTk
import traceback 

live = True
current_step = 0 
detected_step = 0

results = []

result_frame = []

repeat = 1

flag_reset = True

selected_source = None

barcode = ""

started = False

def init(s):
    global self
    self = s 

def is_overall_pass():
    is_pass = True
    try:
        for src_n, src in enumerate(self.Main.results):
            for step_n, step in enumerate(self.Main.results[src_n]):
                for roi_n, roi in enumerate(self.Main.results[src_n][step_n]):
                    roi_pass = roi.get('PASS')
                    if roi_pass is True:
                        is_pass = True
                    else :
                        is_pass = False
                        raise StopIteration
    except StopIteration:
        pass
    return is_pass

def detect(step=None):
    global flag_reset, started
    global current_step
    global detected_step
    global barcode

    if step is not None:
        print("current_step to {}".format(step))
        current_step = step
    
    if flag_reset:
        print("reseting steps")
        reset()

    started = True
    
    detected_step = current_step
    
    if self.MainUi.barcode_entry.get() != "":
        print(self.MainUi.barcode_entry.get())
        barcode = self.MainUi.barcode_entry.get()
    
    detect_next_results = detect_next(step)
    print(f"detect_next_results {detect_next_results}")
    if detect_next_results and step is None:
        next_step()
        

def next_step():
    global detected_step, started
    global current_step
    global flag_reset
    global self

    if flag_reset:
        print("reseting steps")
        reset()
        
    started = True    
    
    detected_step = current_step
    
    current_step = current_step + 1

    if current_step > len(results[0]) - 1:
        current_step = 0
        self.Log.write_log()
        barcode = ""
        self.MainUi.barcode_entry.delete(0, 'end')
        
    print("step increased to current_step {} detected_step {}".format(current_step, detected_step))
        
def reset():
    global current_step, results, result_frame, barcode, started, flag_reset
    
    if started:
        if self.Config.reset_log == "Y":
            self.Log.write_log()
    
    started = False
    current_step = 0    
    barcode = ""
    self.MainUi.barcode_entry.delete(0, 'end')
    
    results.clear()
    for src_n, src in enumerate(self.Profile.loaded_profile):
        results.append([])
        for step_n, step in enumerate(src):
            results[src_n].append([])
            for roi_n, roi in enumerate(step):
                results[src_n][step_n].append(copy.deepcopy(roi))
            
    result_frame.clear()
    for src_n, src in enumerate(self.Profile.loaded_profile):
        result_frame.append([])        
        for step_n, step in enumerate(src):
            result_frame[src_n].append("")
    
    flag_reset = False
    
    print('Reset step!')

def update_view():
    global live
    frames = self.Camera.get_image()
    self.MainUi.update_source(frames)
    #self.MainUi.view.set_image(frames['1'])
    self.MainUi.frm_cams.update(frames)
    if live:
        self.MainUi.view.after(66, update_view)

def detect_next(step=None):
    global current_step, results, result_frame, barcode
    frames = self.Camera.get_image()
    
    is_pass = True
    for src_n, src in enumerate(results):
        frame = copy.deepcopy(list(frames.values())[src_n])
        result_frame[src_n][current_step] = frame
        
        try:
            for roi_n, roi_result in enumerate(results[src_n][current_step]):
                roi_result = self.Process.execute(frame, src_n, current_step, roi_n)
                if not roi_result.get('PASS'):
                    is_pass = False
                if roi_result['type'] == "QR":
                    barcode = str(roi_result.get("CODE"))
        except:
            traceback.print_exc()
            
    if not is_pass:
        self.Com.failed()
            
    if is_pass and step is None: 
        print("Com go next")
        self.Com.go_next()
    elif self.Config.non_stop == "Y":
        print("Non Stop Com go next")
        is_pass = True
        self.Com.go_next()        
    elif not is_pass and step is None:
        print("Com Failed")
        self.Com.failed()
        self.Log.write_log()
    
    return is_pass    
 