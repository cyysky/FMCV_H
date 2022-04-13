from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import cv2
import base64
import copy
from FMCV.Ui.ScrollableFrm  import ScrollableFrame
from FMCV import Util
from FMCV.Ui.ImageViewFrm import ImageView

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

        self.folder_cmb = folder_cmb = ttk.Combobox(setting)
        folder_cmb['values'] = tuple(start.Profile.get_image_folders_list())

        btn_open_folder = Button(setting,text ="Open Folder", command = lambda : start.ActionUi.open_folder(folder_cmb.get()))
        btn_open_folder.pack(side=TOP)

        Label(setting, text = 'Folder/Class').pack()
        btn_save_roi = Button(setting,text ="Save ROI Image To Folder")
        btn_save_roi.pack(side=TOP)
        btn_save_roi.configure(command=self.save_roi_image)   
        folder_cmb.pack()
        

        btn_set_class = Button(setting,text ="Set class")
        btn_set_class.pack(side=TOP)
        btn_set_class.configure(command=self.update_roi_class)   
        self.lbl_class = Label(setting, text = 'Class:')
        self.lbl_class.pack()
        
        self.ai_minimal = ai_minimal = Entry(setting)
        ai_minimal.pack()
        
        
        
        Label(setting, text = 'ROI TYPE').pack()
        self.roi_cmb = roi_cmb = ttk.Combobox(setting,state="readonly")
        roi_cmb['values'] = ("CNN","CON","ANO","QR")
        roi_cmb.pack()
        roi_cmb.current(0)
        roi_cmb.bind("<<ComboboxSelected>>", self.roi_cmb_callback)
        
        Label(setting, text = 'Train CNN').pack()
        train_btn = Button(setting, text ="Train", command = start.ActionUi.cnn_train)
        train_btn.pack(side=TOP)
        
        self.image_view = ImageView(self, relief = GROOVE, borderwidth = 3)
        self.image_view.scale_by = "h"
        
        m1.add(self.image_view, weight = 10)
        m1.add(self.setting_frame, weight = 5)
        
        self.id_picture = -1
        self.image = None
        self.scale = 1
    
        self.scale_by = "w"
        
        self.viewer = self.image_view.viewer
        
        
        if start.Config.mode_name != "ENGINEER":
            self.btn_r_image_update["state"] = DISABLED
            btn_save_roi["state"] = DISABLED
            btn_set_class["state"] = DISABLED
            train_btn["state"] = DISABLED
            ai_minimal["state"] = DISABLED
            
        ai_minimal.bind('<Return>',self.ai_minimal_entry_handler)

    def ai_minimal_entry_handler(*args):
        print(args)
        self.ai_minimal.select_range(0, 'end')
        
    def update_roi_class(self):
        roi_index = self.start.MainUi.roi_index
        if  roi_index > -1:
            self.start.Profile.loaded_profile[self.start.MainUi.cam_pos][self.start.MainUi.cmb_pos][roi_index].update({"class":self.folder_cmb.get()})
            #self.start.MainUi_Refresh.refresh_result_view()
            self.refresh_roi_settings()
    
    def roi_cmb_callback(self,event):
        if self.start.Config.mode_name == "ENGINEER":
            if self.start.MainUi.roi_index > -1:
                self.start.Profile.loaded_profile[self.start.MainUi.cam_pos][self.start.MainUi.cmb_pos][self.start.MainUi.roi_index].update({"type":event.widget.get()})
                #self.start.MainUi_Refresh.refresh_result_view()
        else:
            print("please enable engineer mode")
            
    def refresh_roi_settings(self):
        if self.start.MainUi.roi_index > -1 :
            
            roi = self.start.Profile.loaded_profile[self.start.MainUi.cam_pos][self.start.MainUi.cmb_pos][self.start.MainUi.roi_index]
            
            self.lbl_roi_name.config(text = f"ROI Name : {roi.get('name')}")
            for n, text in enumerate(self.roi_cmb['values']):
                if text == roi.get("type"):
                    self.roi_cmb.current(n)
            self.lbl_class.config(text = f"Class : {roi.get('class')}")
            
            self.ai_minimal.delete(0, END)
            self.ai_minimal.insert(0, str(roi.get("minimal")))
        else:
            self.lbl_roi_name.config(text = "N/A")
            self.lbl_class.config(text = f"Class :")
            
    def save_roi_image(self):
        roi_index = self.start.MainUi.roi_index
        print(roi_index)
        if roi_index > -1:
            self.start.Profile.create_image_folder(self.folder_cmb.get())
            self.folder_cmb['values'] = tuple(self.start.Profile.get_image_folders_list())
            roi = self.start.Profile.loaded_profile[self.start.MainUi.cam_pos][self.start.MainUi.cmb_pos][roi_index]   
            x1 = roi['x1'] 
            y1 = roi['y1'] 
            x2 = roi['x2'] 
            y2 = roi['y2']
            frame = list(self.start.Camera.get_image().values())[self.start.MainUi.cam_pos]
            pth = self.start.Profile.write_image(self.folder_cmb.get(), copy.deepcopy(frame[y1:y2,x1:x2]))
            print(self.folder_cmb.get())
            self.start.MainUi.write(f'ROI Image Saved to {pth}')

    def update_roi_image(self):
        roi_index = self.start.MainUi.roi_index
        if roi_index > -1:
            roi = self.start.Profile.loaded_profile[self.start.MainUi.cam_pos][self.start.MainUi.cmb_pos][roi_index]        
            frame = list(self.start.Camera.get_image().values())[self.start.MainUi.cam_pos]
            x1 = roi['x1'] 
            y1 = roi['y1'] 
            x2 = roi['x2'] 
            y2 = roi['y2']
            roi.update({"image":base64.b64encode(cv2.imencode('.png',copy.deepcopy(frame[y1:y2,x1:x2]))[1]).decode()})
            roi.update({'img':copy.deepcopy(frame[y1:y2,x1:x2])})
            self.set_image(roi['img'])
            self.start.Main.reset()
        else:
            self.clear()

    def get_scale(self):
        if self.image is not None:  
            image_width,image_height = self.image.size
            if self.viewer.winfo_width() > 1:
                self.scale = self.viewer.winfo_width()/image_width
        return self.scale
    
    def set_image(self,image,scale=1):
        self.scale = scale
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.image = Image.fromarray(img)
        
        if self.id_picture > -1:
            self.viewer.image = None
            self.viewer.delete(self.id_picture)

        image_width,image_height = self.image.size
        
        if self.viewer.winfo_width() > 1:
            if self.scale_by == 'w':
                self.scale = self.viewer.winfo_width()/image_width
                if not self.scale == 1:
                    tk_image = self.image.resize((int(image_width*self.scale),int(image_height*self.scale)))
            if self.scale_by == 'h':
                self.scale = self.viewer.winfo_height()/image_height
                if not self.scale == 1:
                    tk_image = self.image.resize((int(image_width*self.scale),int(image_height*self.scale)))
        else:
            tk_image = self.image
        self.viewer.image = ImageTk.PhotoImage(tk_image)
        self.id_picture = self.viewer.create_image(0, 0, image=self.viewer.image, anchor='nw')
        self.viewer.tag_lower(self.id_picture)
        self.viewer.config(scrollregion=self.viewer.bbox('all'))
        
    def clear(self):
        if self.id_picture > -1:
            self.viewer.image = None
            self.viewer.delete(self.id_picture)