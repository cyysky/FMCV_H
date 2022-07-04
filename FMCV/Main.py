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
import time
from threading import Thread

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

last_roi_state = True
last_overall_state = True
continuous_roi_fail_count = 0
continuous_overall_fail_count = 0 

cycle_start_time =  time.time()

def init(s):
    global self, start
    self = s 
    start = s
    
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

def detect(step=None,SN=""):
    global flag_reset, started
    global current_step
    global detected_step
    global barcode
    global cycle_start_time
    global last_overall_state, continuous_overall_fail_count, continuous_roi_fail_count
    
    global platform_non_stop
    
    if start.Config.non_stop  == "Y" and start.Config.platform_model != "NONE":
        platform_non_stop = True
    else:
        platform_non_stop = False
    
    if current_step == 0:
        cycle_start_time =  time.time()

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
    
    if SN != "":
        barcode = SN
        print(f'Incoming {barcode}')

    move_platform_to_position(current_step)

    detect_next_results = start_detect(step)
   
    
    print(f"detect_next_results {detect_next_results}")
    
    if detect_next_results and step is None:
        next_step() #current_step increment
    

        #print(">>{} {}".format(continuous_roi_fail_count, continuous_overall_fail_count))
    
#current_step increment logic
def next_step():
    global last_overall_state, continuous_overall_fail_count   
    global detected_step
    global started
    global current_step
    global flag_reset
    global self
    global barcode
    
    global platform_non_stop

    if flag_reset:
        print("reseting steps")
        reset()
        
    started = True    
    
    detected_step = current_step
    
    current_step = current_step + 1

    if current_step > len(results[0]) - 1:

        current_step = 0
        
        update_total()
        
        start.MainUi.result_frame.set_result(is_overall_pass())
        
        #Continueous fail detection    
        overall_state = is_overall_pass()
        if not overall_state:
            if last_overall_state == False:
                continuous_overall_fail_count += 1
            else:
                continuous_overall_fail_count = 0
        last_overall_state = overall_state
        print(f'the barcode is {barcode}')
        self.Log.write_log()
        
        barcode = ""
        self.MainUi.barcode_entry.delete(0, 'end')
        
        platform_non_stop = False
    
    print("current_step {}".format(current_step))
    
    if platform_non_stop:
        detect()
        
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
            for roi_n, roi in enumerate(step["roi"]):
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

def start_detect(step=None):
    global current_step, results, result_frame, barcode
    global last_roi_state, continuous_roi_fail_count
    global continuous_overall_fail_count, last_overall_state
    
    start.MainUi.result_frame.set_running()
    
    time.sleep(0.350)
    frames = self.Camera.get_image()
    frames = self.Camera.get_image()
    
    is_pass = True
    for src_n, src in enumerate(results):
        frame = copy.deepcopy(list(frames.values())[src_n])
        result_frame[src_n][current_step] = frame
        print(frame.shape)
        try:
            for roi_n, roi_result in enumerate(results[src_n][current_step]):
                roi_result = self.Process.execute(frame, src_n, current_step, roi_n)
                
                if not roi_result.get('PASS'):
                    is_pass = False
                    
                    #Continueous fail detection    
                    if last_roi_state == False:
                        continuous_roi_fail_count += 1
                    else:
                        continuous_roi_fail_count = 0
                last_roi_state = roi_result.get('PASS')
                
                if roi_result['type'] == "QR":
                    barcode = str(roi_result.get("CODE"))

        except:
            traceback.print_exc()
    
    #if not is_pass:
    #    self.Com.failed()
    
    failed_3x = False    
    if start.Config.alarm_if_fail_3x:
        if continuous_roi_fail_count >= 2 :
            print("ROI Failed equal or more then 3 times")
                
        if continuous_overall_fail_count >= 2:
            print("Overall Failed equal or more then 3 times")
            
            if not start.MainUi.ask_reset_continuous_fail_alarm():
                last_overall_state = True
                continuous_overall_fail_count = 0
                failed_3x = True

    if is_pass and step is None: 
        print("Com go next")
        self.Com.go_next()
    elif failed_3x:
        self.Com.failed()
        #self.Com.alarm()
    elif self.Config.non_stop == "Y":
        print("Non Stop Com go next")
        is_pass = True
        self.Com.go_next()        
    elif not is_pass and step is None:
        print("Com Failed")
        self.Com.failed()
        self.Log.write_log()
        #start.MainUi.result_frame.set_result(is_overall_pass())

        if len(results[0]) == 1: # this is a hack for single step application on fail condition to proceed next step when fail
            is_pass = True 
            

    
    return is_pass    
 
def reset_total_count():
    start.Config.class_total.update({"PASS":0,"FAIL":0})
    
def update_total():
    total_pass = start.Config.class_total.get("PASS")
    total_fail = start.Config.class_total.get("FAIL")
    
    if is_overall_pass():
        total_pass = total_pass + 1
    else :
        total_fail = total_fail + 1
    start.Config.class_total.update({"PASS":total_pass,"FAIL":total_fail})


def init_moving_platform():
    """Create instance for moving platform and try to connect to it"""
    print("Initialize moving platform")
    try:
        # Create instance for moving platform and its current position
        start.MovingPlatform = start.Platform.platform_factory(model=start.Config.config['PLATFORM']['model'], feedback_callback=None)
        #start.MovingPlatform = start.Platform.platform_factory(model=start.Config.config['PLATFORM']['model'], feedback_callback=moving_platform_status_feedback_handler)
        self.current_platform_position = start.CartesianPosition()

        # start the auto connect/reconnect thread
        if(start.MovingPlatform is not None):
            self.is_platform_start = True
            self.moving_platform_auto_connect_thread = Thread(target=moving_platform_auto_connect_task, daemon=True)
            self.moving_platform_auto_connect_thread.start()
    except:
        print(f"Initialize moving platform {start.Config.config['PLATFORM']['model']} failed")
        traceback.print_exc()
        pass

def uninit_moving_platform():
    """Stop the autoconnect thread and it will disconnect also"""
    self.is_platform_start = False
    self.moving_platform_auto_connect_thread.join()


def moving_platform_auto_connect_task():
    """Task to auto connect to moving platform's hardware if it is disconnected"""
    print("Start moving platform auto connect task")
    while True:
        if (self.is_platform_start == False):
            # disconnect from the hardware
            start.MovingPlatform.disconnect()
            print(f"Disconnect from {start.Config.config['PLATFORM']['model']}")
            self.MainUi.update_platform_status(is_connected=True, mode=start.MovingPlatform.operating_mode())

            # break the while loop and end the thread
            break

        try:
            if ((start.MovingPlatform.get_is_connected() == False) and self.is_platform_start):
                # try to connect
                print(f"Try to connect to {start.Config.config['PLATFORM']['ip_address']}")
                start.MovingPlatform.connect(start.Config.config['PLATFORM']['ip_address'])

            # check it every 2 seconds
            time.sleep(2)
        except:
            traceback.print_exc()
            print(f"Moving Platform {start.Config.config['PLATFORM']['model']} Connection Error!")

    print("Moving Platform Auto Connect Task Ended")

def moving_platform_status_feedback_handler(position_data):
    # todo: suppose the position is feedback by the callback function, not from the instance
    try:
        self.current_platform_position.set_x(start.MovingPlatform.x())
        self.current_platform_position.set_y(start.MovingPlatform.y())
        self.current_platform_position.set_z(start.MovingPlatform.z())
        self.current_platform_position.set_roll(start.MovingPlatform.roll())

        # call the function in UI module to update the position to UI
        self.MainUi.update_platform_status(is_connected=True, mode=start.MovingPlatform.operating_mode())
    except:
        traceback.print_exc()


def move_platform_to_position(step_index):
    # move the platform to its position
    try:
        # get selected position from profile
        self.platform_position = self.Profile.loaded_profile[self.MainUi.cam_pos][step_index]["platform"]
        print(f"Position: {self.platform_position}")

        x = self.platform_position['x']
        y = self.platform_position['y']
        z = self.platform_position['z']
        roll = self.platform_position['roll']

        if (self.MovingPlatform is not None):
            if (self.MovingPlatform.get_is_connected() == True):
                self.MovingPlatform.move_to_point_sync(x, y, z, roll)

    except Exception as e:
        traceback.print_exc()
        print("Error during reset platform position")