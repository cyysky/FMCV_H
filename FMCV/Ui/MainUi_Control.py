from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import cv2
from FMCV.Ui.ScrollableFrm  import ScrollableFrame
from FMCV import Util
from FMCV.Ui.PlatformSetting import PlatformSettingFrame

from FMCV.Ui.OperatorTop import OperatorWindow

class ControlFrame(ttk.Frame):

    def __init__(self, start, parent, *args, **kwargs):
        #https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application/17470842
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.start = start
        
        sf = ScrollableFrame(self)
        sf.pack(fill = BOTH, expand=True)
        frm = sf.scrollable_frame        
        
        
        
        Label(frm, text = 'Sources').pack()
       
        self.btn_add_source = btn_add_source = Button(frm, text ="Insert Sources")
        btn_add_source.pack(side=TOP)        
        self.btn_remove_source = btn_remove_source = Button(frm, text ="Remove Sources")
        btn_remove_source.pack(side=TOP)
        #cmb_cam.bind("<<ComboboxSelected>>", cmb_callback)
        self.cmb_cam = cmb_cam = ttk.Combobox(frm,state="readonly")
        cmb_cam.pack()
        
        Label(frm, text = 'Steps').pack()
        self.btn_add_step_above = btn_add_step_above = Button(frm, text ="Insert Step")
        btn_add_step_above.pack(side=TOP)
        
        self.btn_add_step = btn_add_step = Button(frm, text ="Add Step")
        btn_add_step.pack(side=TOP)
                
        self.btn_remove_step = btn_remove_step = Button(frm, text ="Remove Step")
        btn_remove_step.pack(side=TOP)
        
        self.cmb = cmb = ttk.Combobox(frm,state="readonly")
        cmb.pack()
        #cmb.bind("<<ComboboxSelected>>", cmb_callback)
        
        
        Label(frm, text = 'ROI Name').pack()
        
        self.roi_entry = roi_entry = Entry(frm)
        roi_entry.pack()
        self.btn_add_roi = btn_add_roi = Button(frm,text ="Add Roi")
        btn_add_roi.pack(side=TOP)

        frm_lbl = Frame(frm)
        frm_lbl.pack()
        self.Lb1 = Lb1 = Listbox(frm_lbl,exportselection=0)
        Lb1.pack(side=LEFT)
        #Lb1.bind("<<ListboxSelect>>", Lbl_callback)
        scrollbar = Scrollbar(frm_lbl)
        scrollbar.pack(side = RIGHT, fill = BOTH)
        Lb1.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = Lb1.yview)
        

        self.btn_remove_roi = btn_remove_roi = Button(frm,text ="Remove Roi")
        btn_remove_roi.pack(side=TOP)
        self.btn_rename_roi = btn_rename_roi = Button(frm,text ="Rename Roi")
        btn_rename_roi.pack(side=TOP)

        Label(frm, text = 'Settings').pack()
        
        save_btn = Button(frm, text ="Save Setting", command = start.ActionUi.save_profile)
        save_btn.pack(side=TOP)
        
        button_1 = Button(frm, text ="Reset Detection Step", command = start.ActionUi.reset_detection_step)
        button_1.pack(side=TOP)
        Label(frm, text = 'Barcode').pack()
        self.barcode_entry = barcode_entry = Entry(frm)
        barcode_entry.pack()
        
        Label(frm, text = 'Detections & Robot').pack()
        button_1 = Button(frm, text ="Detect", command = start.ActionUi.detect)
        button_1.pack(side=TOP)
        button_1 = Button(frm, text ="Detect Selected Step", command = start.ActionUi.detect_current_step)
        button_1.pack(side=TOP)
        self.steps_lbl = Label(frm, text = '')
        self.steps_lbl.pack()
        button_1 = Button(frm, text ="Skip Step", command = start.ActionUi.skip_step)
        button_1.pack(side=TOP)
        button_1 = Button(frm, text ="Robot Next Step", command = start.ActionUi.go_next)
        button_1.pack(side=TOP)

        # Platform setting button
        labelframe_platform = LabelFrame(frm, bd=3, text="Platform")
        labelframe_platform.pack(fill='x', ipadx=10, ipady=10, padx=5, pady=5)
        button_platform_setting = Button(labelframe_platform, text="Setting")
        button_platform_setting.bind("<Button>", lambda e: PlatformSettingFrame(start, start.MainUi.top))
        button_platform_setting.pack(fill='x', ipadx=5, ipady=5, padx=5, pady=5)
        
        #Open new window
        #button_1 = Button(frm, text ="New Window", command = start.ActionUi.go_next)
        #button_1.pack(side=TOP)
        #button_1.bind("<Button>",lambda e: OperatorWindow(start,start.MainUi.top))
        #button_1.pack(side=TOP)
        
        
        if start.Config.mode_name != "ENGINEER":
            btn_add_roi["state"] = DISABLED
            btn_remove_roi["state"] = DISABLED
            btn_rename_roi["state"] = DISABLED
            btn_add_step["state"] = DISABLED
            btn_add_step_above["state"] = DISABLED
            btn_remove_step["state"] = DISABLED
            btn_remove_roi["state"] = DISABLED
            btn_add_source["state"] = DISABLED
            btn_remove_source["state"] = DISABLED
            save_btn["state"] = DISABLED
            
