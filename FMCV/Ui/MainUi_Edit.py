from FMCV.Ui import MainUi as M
from tkinter import messagebox
from tkinter import *
self = M.self

def set_text(entry_widget,text):
    entry_widget.delete(0,END)
    entry_widget.insert(0,text)

def add_roi():
    print(M.roi_entry.get())
    if M.roi_entry.get() == "":
        messagebox.showerror(title="Please enter roi name", message="Please enter roi name")
    else:   
        roi = {   "name":f"{M.roi_entry.get()}",
                         "x1":30,
                         "x2":300 ,
                         "y1":30,
                         "y2":300,
                         "margin" : 0,
                         "smooth" : 0,
                         "precheck" : False,
                         "pre_value" : 0.55,
                         "type":"CNN",
                         "class":"PASS",
                         "minimal":0.95,
                         "return":True
                    }
        self.MainUi_Refresh.move_rectangle(0, 0, 100, 100)
        self.Profile.add_roi(M.cam_pos,M.cmb_pos, M.roi_index, roi)
        self.MainUi_Refresh.refresh_listbox()
        self.MainUi.t_view.update_roi_image()
        self.Main.flag_reset = True
        self.Profile.flag_save = True
        #set_text(M.roi_entry,"")
    
def remove_roi():
    if M.roi_index != -1:
        self.Profile.remove_roi(M.cam_pos,M.cmb_pos, M.roi_index)
        self.MainUi_Refresh.refresh_listbox()
        self.Main.flag_reset = True
        self.Profile.flag_save = True

def add_source():
    self.Profile.add_source(M.cam_pos)
    M.cam_pos = M.cam_pos + 1
    self.MainUi_Refresh.refresh_source_cmb()
    self.MainUi_Refresh.refresh_step_cmb()
    self.MainUi_Refresh.refresh_listbox()
    self.Main.flag_reset = True
    self.Profile.flag_save = True

def remove_source():
    self.Profile.remove_source(M.cam_pos)
    M.cmb_pos = M.cmb_pos - 1
    if M.cmb_pos < 0:
        M.cmb_pos = 0
        
    self.MainUi_Refresh.refresh_source_cmb()
    self.MainUi_Refresh.refresh_step_cmb()
    self.MainUi_Refresh.refresh_listbox()
    self.Main.flag_reset = True
    self.Profile.flag_save = True

def add_step():
    self.Profile.add_step(M.cam_pos,M.cmb_pos)
    M.cmb_pos = M.cmb_pos + 1
    
    self.MainUi_Refresh.refresh_source_cmb()
    self.MainUi_Refresh.refresh_step_cmb()
    self.MainUi_Refresh.refresh_listbox()
    self.Main.flag_reset = True
    self.Profile.flag_save = True
    
def add_step_above():
    self.Profile.insert_step(M.cam_pos,M.cmb_pos)
    #M.cmb_pos = M.cmb_pos + 1
    
    self.MainUi_Refresh.refresh_source_cmb()
    self.MainUi_Refresh.refresh_step_cmb()
    self.MainUi_Refresh.refresh_listbox()
    self.Main.flag_reset = True
    self.Profile.flag_save = True
    
def remove_step():
    self.Profile.remove_step(M.cam_pos,M.cmb_pos)
    M.cmb_pos = M.cmb_pos - 1
    if M.cmb_pos < 0:
        M.cmb_pos = 0        
    self.MainUi_Refresh.refresh_source_cmb()
    self.MainUi_Refresh.refresh_step_cmb()
    self.MainUi_Refresh.refresh_listbox()
    self.Main.flag_reset = True
    self.Profile.flag_save = True

def btn1_clicked(event):

    M.lx,M.ly = (M.view.viewer.canvasx(event.x), M.view.viewer.canvasy(event.y))
    
    roi = self.Profile.loaded_profile[M.cam_pos][M.cmb_pos]["roi"][M.roi_index]
    M.lx1 = roi['x1'] 
    M.ly1 = roi['y1'] 
    M.lx2 = roi['x2'] 
    M.ly2 = roi['y2'] 
    
    plx = int(M.lx/M.view.scale)
    ply = int(M.ly/M.view.scale)
    
    if M.roi_index > -1:
        scale = M.view.get_scale()
        roi = self.Profile.loaded_profile[M.cam_pos][M.cmb_pos]["roi"][M.roi_index]

        x1 = roi['x1'] * scale
        y1 = roi['y1'] * scale
        x2 = roi['x2'] * scale
        y2 = roi['y2'] * scale
        
        if M.lx >= x1 and M.lx <= x2 - 20 and M.ly >= y1 and M.ly <= y2 - 20:
            M.mv_type = "move"
        elif M.lx > x2 - 20 and M.lx <= x2 and M.ly > y2 - 20 and M.ly < y2:
            M.mv_type = "resize"
        else:
            M.mv_type = ""
        print(f'mv_type = {M.mv_type}')
        

def btn1_move(event):    
    x,y = (M.view.viewer.canvasx(event.x), M.view.viewer.canvasy(event.y))
    
    px = int(x/M.view.scale)
    py = int(y/M.view.scale)
    plx = int(M.lx/M.view.scale)
    ply = int(M.ly/M.view.scale)
    
    if M.roi_index > -1:
        roi = self.Profile.loaded_profile[M.cam_pos][M.cmb_pos]["roi"][M.roi_index]

        rx1 = roi['x1'] 
        ry1 = roi['y1'] 
        rx2 = roi['x2'] 
        ry2 = roi['y2'] 
        
        if M.mv_type == "move":
            roi['x1'] = int(M.lx1 + px - plx) 
            roi['y1'] = int(M.ly1 + py - ply) 
            roi['x2'] = int(M.lx2 + px - plx) 
            roi['y2'] = int(M.ly2 + py - ply) 
            self.Main.flag_reset = True
            self.Profile.flag_save = True
            
        if M.mv_type == "resize":
            roi['x2'] = int(M.lx2 + px - plx)
            roi['y2'] = int(M.ly2 + py - ply)
            self.Main.flag_reset = True
            self.Profile.flag_save = True
            
        self.MainUi_Refresh.refresh_edit_roi_rectangle()
        
def rename_roi(): 
    if M.roi_entry.get() == "":
        messagebox.showerror(title="Please enter roi name", message="Please enter roi name")
    else:   
        self.Profile.update_roi(M.cam_pos,M.cmb_pos, M.roi_index,{"name":f"{M.roi_entry.get()}"})
        self.MainUi_Refresh.refresh_listbox()
        self.MainUi_Refresh.refresh_edit_roi_rectangle()
        self.MainUi_Refresh.display_roi_image()
        M.t_view.refresh_roi_settings()
        self.MainUi_Refresh.refresh_result_view()
        
M.view.viewer.bind("<B1-Motion>", btn1_move)   
M.view.viewer.bind("<Button-1>", btn1_clicked)   
     
M.btn_add_roi.configure(command=add_roi) 
M.btn_remove_roi.configure(command=remove_roi) 
M.btn_rename_roi.configure(command=rename_roi)

M.btn_add_step.configure(command=add_step) 
M.btn_add_step_above.configure(command=add_step_above)
M.btn_remove_step.configure(command=remove_step) 

M.btn_add_source.configure(command=add_source) 
M.btn_remove_source.configure(command=remove_source) 
