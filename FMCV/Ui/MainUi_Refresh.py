from FMCV.Ui import MainUi as M
from tkinter import *
self = M.self
import base64
import copy
import cv2
import traceback

def refresh_edit_roi_rectangle():
    if M.roi_index > -1:
        #print(f'step_cmb_pos {M.cmb_pos} roi_cmb_pos {M.roi_index}')
        scale = M.view.get_scale()
        roi = self.Profile.loaded_profile[M.cam_pos][M.cmb_pos][M.roi_index]        
        move_rectangle(roi['x1']*scale, roi['y1']*scale, roi['x2']*scale, roi['y2']*scale)
    else:
        remove_rectangle()
        
def remove_rectangle():
    move_rectangle(-1,-1,-1,-1)
        
def move_rectangle(x1, y1, x2, y2):
    if M.id_rect == -1:
        M.id_rect = M.view.viewer.create_rectangle(x1, y1, x2, y2,outline='orange')
        print(f'id_rect = {M.id_rect}')
    else:
        M.view.viewer.coords(M.id_rect, x1, y1, x2, y2)

def refresh_listbox(pos = -1):
    remove_rectangle()
    refresh_step_cmb()
    if pos == -1:
        pos = M.cmb_pos
    M.Lb1.delete(0,END)
    try:
        for roi_n, roi in enumerate(self.Profile.loaded_profile[M.cam_pos][pos]):
            M.Lb1.insert(roi_n, roi['name'])
    except:
        print("Empty source and position")
        
def refresh_result_view(pos = -1):   
    if pos == -1:
        pos = M.cmb_pos
    M.r_view.viewer.delete("all")
    M.result_frame.set_result(None)
    try:
        
        scale = M.r_view.get_scale()

        for roi_n, roi in enumerate(self.Main.results[M.cam_pos][pos]): 
            #print(f"{roi['name']} {roi['PASS']}")
            roi_pass = roi.get('PASS')
            if roi_pass is True:
                color = 'green'
            else:
                color = 'red'
            M.r_view.viewer.create_rectangle(roi['x1'] * scale, roi['y1'] * scale, roi['x2'] * scale, roi['y2'] * scale , outline=color,  tags=(str(roi_n)))
        
        M.result_frame.set_result(self.Main.is_overall_pass())
        M.r_view.set_image(self.Main.result_frame[M.cam_pos][pos])
        M.r_view.current_results = self.Main.results[M.cam_pos][pos]
        
    except:
        #traceback.print_exc()
        print("refresh_result_view: didn't have results ")
    
def refresh_step_cmb():
    try:
        step_list = []
        for step_n, step in enumerate(self.Profile.loaded_profile[M.cam_pos]):
            step_list.append(step_n+1)
        M.cmb['values'] = tuple(step_list)
        M.cmb.current(M.cmb_pos)
    except:
        print("Empty step of source")
        
def refresh_source_cmb():
    source_list = []
    for src_n, src in enumerate(self.Profile.loaded_profile):
        source_list.append(src_n+1)
    if len(source_list) > 0:
        M.cmb_cam['values'] = tuple(source_list)
    else:
        M.cmb_cam['values'] = tuple([0])
    M.cmb_cam.current(M.cam_pos)


def display_roi_image():
    if M.roi_index > -1:
        roi = self.Profile.loaded_profile[M.cam_pos][M.cmb_pos][M.roi_index]
        if roi.get('img') is not None:
            print("display image")
            M.t_view.set_image(roi['img'])
    else:
        M.t_view.clear()


#refresh_cmb_cam()
refresh_source_cmb()
refresh_step_cmb()
refresh_listbox()


