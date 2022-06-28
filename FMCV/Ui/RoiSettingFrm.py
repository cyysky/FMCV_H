from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import cv2
import base64
import copy
from FMCV.Ui.ScrollableFrm  import ScrollableFrame
from FMCV import Util
from FMCV.Ui.ImageViewFrm import ImageView
from FMCV.Ui.RoiSettingCnnFrm import ROISettingCNNFrame
from FMCV.Ui.RoiSettingFiducialFrm import ROISettingFiducialFrame

class ROISettingFrame(ttk.Frame):

    def __init__(self,start, parent, *args, **kwargs):
        #https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application/17470842
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.start = start
        
        m1 = ttk.PanedWindow(self,orient=HORIZONTAL)
        m1.pack(fill=BOTH, expand=True)
        
        self.setting_frame = ScrollableFrame(m1)
        self.setting = setting = self.setting_frame.scrollable_frame
        
        self.lbl_roi_name = Label(setting, text = 'N/A')
        self.lbl_roi_name.pack()
        
        self.btn_r_image_update = Button(setting,text ="Roi Image Update")
        self.btn_r_image_update.pack(side=TOP)
        self.btn_r_image_update.configure(command=self.update_roi_image) 
        
        Label(setting, text = 'ROI TYPE').pack()
        self.roi_cmb = roi_cmb = ttk.Combobox(setting,state="readonly")
        roi_cmb['values'] = ("CNN","CON","FIDUCIAL","ANO","QR")
        roi_cmb.pack()
        roi_cmb.current(0)
        roi_cmb.bind("<<ComboboxSelected>>", self.roi_type_cmb_callback)
        
        #CNN Frame
        self.cnn_frame = cnn_frame = ROISettingCNNFrame(self.start,setting)
        
        #Fiducial Frame
        self.fiducial_frame = cnn_frame = ROISettingFiducialFrame(self.start,setting)
        
        self.image_view = ImageView(self, relief = GROOVE, borderwidth = 3)
        
        m1.add(self.image_view, weight = 10)
        m1.add(self.setting_frame, weight = 5)
        
        self.id_picture = -1
        self.image = None
        self.scale = 1
    
        self.scale_by = "w"
        
        #self.viewer = self.image_view.viewer
        
        #Disable button when is not ENGINEERING mode
        if start.Config.mode_name != "ENGINEER":
            self.btn_r_image_update["state"] = DISABLED
            
    def roi_type_cmb_callback(self,event):
        if self.start.Config.mode_name == "ENGINEER":
            if self.start.MainUi.roi_index > -1:
                self.start.Profile.loaded_profile[self.start.MainUi.cam_pos][self.start.MainUi.cmb_pos]["roi"][self.start.MainUi.roi_index].update({"type":event.widget.get()})
                #self.start.MainUi_Refresh.refresh_result_view()
                
                self.start.Main.flag_reset = True
                self.start.Profile.flag_save = True
        else:
            print("please enable engineer mode")
        self.display_roi_type_widget()
            
    def clear_roi_type_widget(self):
        self.cnn_frame.pack_forget()
        self.fiducial_frame.pack_forget()

    def display_roi_type_widget(self):        
        self.clear_roi_type_widget()
        if self.start.MainUi.roi_index > -1:
            roi_type = self.start.Profile.loaded_profile[self.start.MainUi.cam_pos][self.start.MainUi.cmb_pos]["roi"][self.start.MainUi.roi_index].get('type')
            if roi_type == "CNN":
                self.cnn_frame.pack(fill=BOTH, expand=True)
                self.cnn_frame.refresh()
            if roi_type == "FIDUCIAL":
                self.fiducial_frame.pack(fill=BOTH, expand=True)
                self.fiducial_frame.refresh()
            
            
    def refresh_roi_settings(self):
        if self.start.MainUi.roi_index > -1 :
            
            roi = self.start.Profile.loaded_profile[self.start.MainUi.cam_pos][self.start.MainUi.cmb_pos]["roi"][self.start.MainUi.roi_index]
            
            self.lbl_roi_name.config(text = f"ROI Name : {roi.get('name')}")
            
            for n, text in enumerate(self.roi_cmb['values']):
                if text == roi.get("type"):
                    self.roi_cmb.current(n)
                    
            self.display_roi_type_widget()
        else:
            self.lbl_roi_name.config(text = "N/A")
            

            
    def update_roi_image(self):
        roi_index = self.start.MainUi.roi_index
        if roi_index > -1:
            roi = self.start.Profile.loaded_profile[self.start.MainUi.cam_pos][self.start.MainUi.cmb_pos]["roi"][roi_index]
            frame = list(self.start.Camera.get_image().values())[self.start.MainUi.cam_pos]
            x1 = roi['x1'] 
            y1 = roi['y1'] 
            x2 = roi['x2'] 
            y2 = roi['y2']
            roi.update({"image":base64.b64encode(cv2.imencode('.png',copy.deepcopy(frame[y1:y2,x1:x2]))[1]).decode()})
            roi.update({'img':copy.deepcopy(frame[y1:y2,x1:x2])})
            self.image_view.set_image(roi['img'])
            self.start.Main.flag_reset = True
        else:
            self.image_view.clear()