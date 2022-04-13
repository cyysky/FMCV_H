import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from FMCV.Ui.ImageViewFrm import ImageView
from FMCV.Ui.ResultsFrm import ResultsFrame
from FMCV.Ui.ScrollableFrm  import ScrollableFrame
from FMCV.Ui.RoiSettingFrm import ROISettingFrame
from FMCV.Ui.CamerasFrm import CamerasFrame
from FMCV.Ui.MainUi_Control import ControlFrame

from tkinter import messagebox

top = Tk()

roi_index = -1
cmb_pos = 0
cam_pos = 0

id_rect = -1
# Code to add widgets will go here...
lx = -1
ly = -1

mv_type = ""
window_width, window_height = 0, 0
 
def on_closing():
    global self
    global top
    # lambda e: top.quit()
    if self.Profile.flag_save:
        if messagebox.askokcancel("Save", "Do you want to save settings?"):
            self.Profile.write()
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        top.destroy()
 
def init(s):
    global self
    self = s 
    start = s 
    
    global top, view, r_view, t_view
    
    global Lb1, cmb_cam, cmb, roi_entry, barcode_entry
    
    global btn_add_roi, btn_remove_roi, btn_rename_roi
    
    global btn_add_step, btn_remove_step, btn_add_step_above
    
    global btn_add_source, btn_remove_source
    
    global result_frame
    
    global statusbar
    
    global frm_cams
    
    global steps_lbl
    
    # https://stackoverflow.com/questions/15981000/tkinter-python-maximize-window
    w = top.winfo_screenwidth()
    if os.name == 'nt':
        top.state('zoomed')
        h = top.winfo_screenheight() - 30
    else:
        h = top.winfo_screenheight() - 65
    top.geometry("{}x{}-0+0".format(w, h))   
    top.lift()
    top.attributes('-topmost', 1)
    top.attributes('-topmost', 0)
    
    top.title("FMCV H Profile:{}".format(self.Config.profile))
    
    statusbar = Label(top, text="FMCV H 20220220 22:22", bd=1, relief=SUNKEN, anchor=W)
    statusbar.pack(side=BOTTOM, fill=X)
    
    m1 = ttk.PanedWindow(top, orient=HORIZONTAL)
    m1.pack(fill=BOTH, expand=True)
    
    paned_left = ttk.PanedWindow(m1, orient=HORIZONTAL)
    #paned_left.pack(fill=BOTH, expand=True)
    
    cf = ControlFrame(self,paned_left)
    Lb1 = cf.Lb1
    Lb1.bind("<<ListboxSelect>>", Lbl_callback)
    cmb_cam = cf.cmb_cam
    cmb_cam.bind("<<ComboboxSelected>>", cmb_callback)
    cmb = cf.cmb
    cmb.bind("<<ComboboxSelected>>", cmb_callback)
    roi_entry = cf.roi_entry
    btn_add_roi = cf.btn_add_roi
    btn_remove_roi = cf.btn_remove_roi
    btn_rename_roi = cf.btn_rename_roi
    btn_add_step = cf.btn_add_step
    btn_add_step_above = cf.btn_add_step_above
    btn_remove_step = cf.btn_remove_step
    btn_add_source = cf.btn_add_source
    btn_remove_source = cf.btn_remove_source
    steps_lbl = cf.steps_lbl
    barcode_entry = cf.barcode_entry
    

    
    frm_cams = CamerasFrame(start, paned_left)

    m2 = ttk.PanedWindow(m1, orient=VERTICAL)
    
    m3 = ttk.PanedWindow(m2, orient=HORIZONTAL)
    m4 = ttk.PanedWindow(m2, orient=HORIZONTAL)
    
    r_view = ImageView(m2, relief = GROOVE, borderwidth = 3)
    view  = ImageView(m2, relief = GROOVE, borderwidth = 3)

    m3.add(view, weight=1)
    m3.add(r_view, weight=1)
    
    t_view = ROISettingFrame(self,m4)
    t_view.scale_by = "h"

    result_frame = ResultsFrame(start,m4)
    
    m4.add(t_view, weight=10)
    m4.add(result_frame, weight=12)
    
    m2.add(m3, weight=1)
    m2.add(m4, weight=1)
    
    paned_left.add(cf, weight = 10)
    paned_left.add(frm_cams, weight = 7)
    
    m1.add(paned_left,weight=25)
    m1.add(m2,weight=100)
    
    top.protocol("WM_DELETE_WINDOW", on_closing)
    top.bind('<Escape>',lambda v: on_closing())
    top.bind("<Configure>", configure_event)
    top.bind()
    top.bind('<Return>',barcode_entry_handler)

def barcode_entry_handler(*args):
    #print(args)
    barcode_entry.select_range(0, 'end')

def write(text):
    global statusbar
    statusbar.config(text=text)

def cmb_callback(event):
    global cmb_pos, cam_pos
    cam_pos = cmb_cam.current()
    #cmb_pos = event.widget.current()
    cmb_pos = cmb.current()
    #print(event.widget.current(), event.widget.get())
    #print(cam_pos,cmb_pos)
    
    self.MainUi_Refresh.refresh_listbox()
    self.MainUi_Refresh.refresh_result_view()
    

def Lbl_callback(event):
    global roi_index
    selection = event.widget.curselection()
    if selection:
        roi_index = selection[0]
        data = event.widget.get(roi_index)
        #print(data)
        self.MainUi_Refresh.refresh_edit_roi_rectangle()
        self.MainUi_Refresh.display_roi_image()
        t_view.refresh_roi_settings()
    else:
        roi_index = -1
    #print(f'roi_index = {roi_index}')

def configure_event(event):
    #https://stackoverflow.com/questions/61712329/tkinter-track-window-resize-specifically
    global window_width, window_height
    if event.widget == top:
        if (window_width != event.width) and (window_height != event.height):
            window_width, window_height = event.width,event.height
            print(f"The width of Toplevel is {window_width} and the height of Toplevel "
                  f"is {window_height}")
                  
    self.MainUi_Refresh.refresh_edit_roi_rectangle()
    
    if top.state() == 'zoomed':
        #print("My window is maximized")
        pass
    if top.state() == 'normal':
        #print("My window is normal")
        pass
        
def update_source(frames):
    global cam_pos, view
    try:
        view.set_image(list(frames.values())[cam_pos])
    except:
        traceback.print_exc()