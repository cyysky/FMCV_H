from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import cv2
from FMCV.Ui.ScrollableFrm  import ScrollableFrame
from FMCV import Util

class ResultsFrame(ttk.Frame):

    def __init__(self, start, parent, *args, **kwargs):
        #https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application/17470842
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.start = start
        
        m1 = ttk.PanedWindow(self,orient=HORIZONTAL)
        m1.pack(fill=BOTH, expand=True)
        
        tree = ttk.Treeview(m1, column=("Items", "Values"), show='headings' , height=5)
        tree.column("# 1", anchor=CENTER, width=20)
        tree.heading("# 1", text="Items")
        tree.column("# 2", anchor=CENTER,  width=40)
        tree.heading("# 2", text="Values")
        
        for i in range(50):
            tree.insert('', 'end', text="1", values=("", ""))
            
        tree.pack(expand=True,fill=Y)
        # Constructing vertical scrollbar
        # with treeview
        verscrlbar = ttk.Scrollbar(tree, orient ="vertical", command = tree.yview)
         
        # Calling pack method w.r.to vertical
        # scrollbar
        verscrlbar.pack(side ='right', fill ='y')
        tree.configure(yscrollcommand = verscrlbar.set)
        
        self.result_frame = ScrollableFrame(m1)
        self.content = content = self.result_frame.scrollable_frame
        
        self.lbl_result = Label(self.content,width = 30 , height = 8, text = 'RESULT')
        self.lbl_result.pack()
        
        self.lbl_stat = Label(self.content,width = 15 , height = 4, text = "Total PASS : 0 \nTotal FAIL : 0")
        self.lbl_stat.pack()
        
        self.update_total()
        
        Label(content, text = 'Folder').pack()
        self.folder_cmb = folder_cmb = ttk.Combobox(content)
        folder_cmb['values'] = tuple(start.Profile.get_image_folders_list())
        folder_cmb.pack()
        
        self.btn_save_result_roi_image = btn_save_result_roi_image = Button(content,text ="Save Result Image To Folder")
        btn_save_result_roi_image.pack()
        btn_save_result_roi_image.configure(command=self.save_result_roi_image)
        
        self.btn_open_folder = Button(content,text ="Open Folder", command = lambda:start.ActionUi.open_folder(folder_cmb.get()))
        self.btn_open_folder.pack()
        
        self.tree = tree
        
        m1.add(tree,weight=1)
        m1.add(self.result_frame,weight=3)
        
        self.result_roi = {}
     
    def save_result_roi_image(self):
        img = self.result_roi.get('result_image')
        if img is not None:
            self.start.Profile.create_image_folder(self.folder_cmb.get())
            pth = self.start.Profile.write_image(self.folder_cmb.get(),img)
            print(self.folder_cmb.get())
            self.start.MainUi.write(f'Result Image Saved to {pth}')



    def update_results(self,roi_results):  
        
        self.tree.delete(*self.tree.get_children())   
        
        # for widgets in self.result_frame.scrollable_frame.winfo_children():
            # widgets.destroy()

        for roi_name, roi_value in Util.without_keys(roi_results,{"img","image","result_image"}).items():
            
            self.tree.insert('', 'end', text="1", values=(roi_name, roi_value))
            #ttk.Label(self.content, text=str(roi_attrib)).pack()
    
    def set_result(self,is_pass):
        if is_pass is None:
            self.lbl_result.config(bg='SystemButtonFace',text="RESET")
            self.update_total()
        else:
            if is_pass:
                color = 'green'
                msg = 'PASS'
            else:
                color = 'red'
                msg = 'FAIL'
            self.lbl_result.config(bg=color,text=msg)
        
    def update_total(self):
        total_pass = self.start.Config.class_total.get("PASS")
        total_fail = self.start.Config.class_total.get("FAIL")
        self.lbl_stat.config(text = f"Total PASS : {total_pass}\nTotal FAIL : {total_fail}")
     
