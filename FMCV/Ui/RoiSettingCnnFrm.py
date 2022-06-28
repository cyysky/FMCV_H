from tkinter import *
from tkinter import ttk
import copy

class ROISettingCNNFrame(ttk.Frame):

    def __init__(self, start, parent, *args, **kwargs):
        #https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application/17470842
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.start = start
        
        #CNN Frame
        cnn_frame = self
        
        self.folder_cmb = folder_cmb = ttk.Combobox(cnn_frame)
        folder_cmb['values'] = tuple(start.Profile.get_image_folders_list())

        btn_open_folder = Button(cnn_frame,text ="Open Folder", command = lambda : start.ActionUi.open_folder(folder_cmb.get()))
        btn_open_folder.pack(side=TOP)

        Label(cnn_frame, text = 'Folder/Class').pack()
        btn_save_roi = Button(cnn_frame,text ="Save ROI Image To Folder")
        btn_save_roi.pack(side=TOP)
        btn_save_roi.configure(command=self.save_roi_image)   
        folder_cmb.pack()
        

        btn_set_class = Button(cnn_frame,text ="Set class")
        btn_set_class.pack(side=TOP)
        btn_set_class.configure(command=self.update_roi_class)   
        self.lbl_class = Label(cnn_frame, text = 'Class:')
        self.lbl_class.pack()
        
        self.ai_minimal = ai_minimal = Entry(cnn_frame)
        ai_minimal.pack()
        
        Label(cnn_frame, text = 'Train CNN').pack()
        train_btn = Button(cnn_frame, text ="Train", command = start.ActionUi.cnn_train)
        train_btn.pack(side=TOP)
        
        ai_minimal.bind('<Return>',self.ai_minimal_entry_handler)
        
        if start.Config.mode_name != "ENGINEER":
            btn_save_roi["state"] = DISABLED
            btn_set_class["state"] = DISABLED
            train_btn["state"] = DISABLED
            ai_minimal["state"] = DISABLED

    def ai_minimal_entry_handler(*args):
        print(args)
        self.ai_minimal.select_range(0, 'end')
        
    def update_roi_class(self):
        roi_index = self.start.MainUi.roi_index
        if  roi_index > -1:
            self.start.Profile.loaded_profile[self.start.MainUi.cam_pos][self.start.MainUi.cmb_pos]["roi"][roi_index].update({"class":self.folder_cmb.get()})
            #self.start.MainUi_Refresh.refresh_result_view()
            self.start.MainUi.t_view.refresh_roi_settings()
            
    def save_roi_image(self):
        roi_index = self.start.MainUi.roi_index
        print(roi_index)
        if roi_index > -1:
            self.start.Profile.create_image_folder(self.folder_cmb.get())
            self.folder_cmb['values'] = tuple(self.start.Profile.get_image_folders_list())
            roi = self.start.Profile.loaded_profile[self.start.MainUi.cam_pos][self.start.MainUi.cmb_pos]["roi"][roi_index]
            x1 = roi['x1'] 
            y1 = roi['y1'] 
            x2 = roi['x2'] 
            y2 = roi['y2']
            frame = list(self.start.Camera.get_image().values())[self.start.MainUi.cam_pos]
            pth = self.start.Profile.write_image(self.folder_cmb.get(), copy.deepcopy(frame[y1:y2,x1:x2]))
            print(self.folder_cmb.get())
            self.start.MainUi.write(f'ROI Image Saved to {pth}')
    
    def refresh(self):
        if self.start.MainUi.roi_index > -1 :
            
            roi = self.start.Profile.loaded_profile[self.start.MainUi.cam_pos][self.start.MainUi.cmb_pos]["roi"][self.start.MainUi.roi_index]
           
            self.lbl_class.config(text = f"Class : {roi.get('class')}")
            
            self.ai_minimal.delete(0, END)
            self.ai_minimal.insert(0, str(roi.get("minimal")))
        else:
            self.lbl_class.config(text = f"Class : N/A")