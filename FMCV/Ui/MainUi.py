import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import askokcancel, showinfo, WARNING
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
    
    statusbar = Label(top, text="FMCV H {}".format(start.Config.version), bd=1, relief=SUNKEN, anchor=W)
    statusbar.pack(side=BOTTOM, fill=X)
    
    m1 = ttk.PanedWindow(top, orient=HORIZONTAL)
    m1.pack(fill=BOTH, expand=True)
    
    paned_left = ttk.PanedWindow(m1, orient=HORIZONTAL)
    
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

    result_frame = ResultsFrame(start,m4)
    
    m4.add(t_view, weight=10)
    m4.add(result_frame, weight=12)

    bottom_frame = ttk.PanedWindow(m2, orient=HORIZONTAL)
    platform_control_frame = LabelFrame(bottom_frame, text="Platform Control")
    bottom_frame.add(platform_control_frame, weight=1)
    platform_control_frame.columnconfigure(0, weight=1)
    platform_control_frame.columnconfigure(1, weight=1)
    platform_control_frame.columnconfigure(2, weight=1)
    platform_control_frame.columnconfigure(3, weight=1)


    self.platform_mode = StringVar()
    self.platform_mode_label = Label(platform_control_frame, textvariable=self.platform_mode)
    self.platform_mode_label.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
    self.platform_enable_button = Button(platform_control_frame, text="Enable Platform", command=toggle_platform_mode)
    self.platform_enable_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
    self.platform_clear_error_button = Button(platform_control_frame, text="Clear Error", command=clear_platform_error)
    self.platform_clear_error_button.grid(row=0, column=2, padx=5, pady=5, sticky='ew')
    self.platform_reset_button = Button(platform_control_frame, text="Reset", command=reset_platform)
    self.platform_reset_button.grid(row=0, column=3, padx=5, pady=5, sticky='ew')


    m2.add(m3, weight=10)
    m2.add(m4, weight=10)
    if start.Config.platform_model != "NONE":
        m2.add(bottom_frame, weight=1)
    
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

    self.Main.move_platform_to_position(cmb_pos)
    pass
    

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
        print("update source exception")
        traceback.print_exc()
        
def ask_reset_continuous_fail_alarm():
    answer = askokcancel(title='Alert',
        message='Fail 3 times, still continue?',
        icon=WARNING)
    return answer
        # showinfo(
            # title='Deletion Status',
            # message='The data is deleted successfully')

def update_platform_status(is_connected=False, mode=""):
    """Get the platform status from Main.py and update it to UI"""
    # update connection status and mode to UI
    if (mode is not None):
        self.platform_mode.set(mode)
        if (mode == "MODE_DISABLED"):
            self.platform_mode_label.config(bg="#ff0000", fg="#ffffff")
        elif (mode == "MODE_ENABLE"):
            self.platform_mode_label.config(bg="#23ff23", fg="#000000")
    pass

def toggle_platform_mode():
    """Enable/disable platform operating mode"""
    if (self.MovingPlatform.get_is_enabled() == True):
        self.MovingPlatform.disable_platform()
        self.platform_enable_button.config(text="Enable Platform")
    else:
        self.MovingPlatform.enable_platform()
        self.platform_enable_button.config(text="Disable Platform")
    pass

def clear_platform_error():
    """Clear error"""
    self.MovingPlatform.clear_error()
    pass


def reset_platform():
    """Reset platform"""
    self.MovingPlatform.reset()
    pass