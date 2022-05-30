from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import copy


class ROISettingFiducialFrame(ttk.Frame):

    def __init__(self, start, parent, *args, **kwargs):
        #https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application/17470842
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.start = start
        
       
        Label(self, text = 'Fiducial margin pixel').pack()
        self.margin_entry = margin = Entry(self)
        margin.pack()
        margin.bind('<Return>',self.save)
        
        Label(self, text = 'Minimal Score').pack()
        self.minimal_entry = minimal_entry = Entry(self)
        minimal_entry.pack()
        minimal_entry.bind('<Return>',self.save)
        
        btn_save = Button(self,text ="Save")
        btn_save.pack(side=TOP)
        btn_save.configure(command=self.save)   
        

        
        if start.Config.mode_name != "ENGINEER":
            btn_save_roi["state"] = DISABLED
            btn_set_class["state"] = DISABLED
            train_btn["state"] = DISABLED
            ai_minimal["state"] = DISABLED

    def save(self):
        roi_index = self.start.MainUi.roi_index
        if  roi_index > -1:
            try:            
                print(int(self.margin_entry.get()))
                self.start.Profile.loaded_profile[self.start.MainUi.cam_pos][self.start.MainUi.cmb_pos][roi_index].update({"margin":int(self.margin_entry.get())})
            except:
                messagebox.showwarning("Please key-in margin integer only", "Warning")
            try:            
                print(float(self.minimal_entry.get()))
                self.start.Profile.loaded_profile[self.start.MainUi.cam_pos][self.start.MainUi.cmb_pos][roi_index].update({"minimal":float(self.minimal_entry.get())})
            except:
                messagebox.showwarning("Please key-in minimal decimal only 0.0 - 1.0", "Warning")
        else:
            messagebox.showwarning("Please select roi on left", "Warning")
        self.start.MainUi.t_view.refresh_roi_settings()
    
    def refresh(self):
        if self.start.MainUi.roi_index > -1 :
            
            roi = self.start.Profile.loaded_profile[self.start.MainUi.cam_pos][self.start.MainUi.cmb_pos][self.start.MainUi.roi_index]

            self.margin_entry.delete(0, END)
            self.margin_entry.insert(0, str(roi.get("margin")))
            
            self.minimal_entry.delete(0, END)
            self.minimal_entry.insert(0, str(roi.get("minimal")))
        else:
            self.lbl_class.config(text = f"Class : N/A")