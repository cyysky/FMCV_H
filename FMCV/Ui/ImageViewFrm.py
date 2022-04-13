from tkinter import *
from PIL import ImageTk, Image
import cv2
import traceback
class ImageView(Frame):

    def __init__(self, parent, *args, **kwargs):
        #https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application/17470842
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        hbar=Scrollbar(self,orient=HORIZONTAL, width=20)
        hbar.pack(side=BOTTOM,fill=X)
        
        vbar=Scrollbar(self,orient=VERTICAL, width=20)
        vbar.pack(side=RIGHT,fill=Y)
        
        self.viewer = Canvas(self,width=100,height=300,scrollregion=(0,0,640,480))

        vbar.config(command=self.viewer.yview)      
        hbar.config(command=self.viewer.xview)  
        
        self.viewer.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.viewer.pack(expand=True,fill=BOTH)
        
        self.id_picture = -1
        self.image = None
        self.scale = 1
    
        self.scale_by = "w"
    
    def get_scale(self):
        if self.image is not None:  
            image_width,image_height = self.image.size
            if self.viewer.winfo_width() > 1:
                self.scale = self.viewer.winfo_width()/image_width
        return self.scale
    
    def set_image(self,image,scale=1):
        try:
            self.scale = scale
            if image is not None:
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
            else:
                print("set_image image is None")
        except:
            traceback.print_exc()

    def lower_image_in_viewer(self):
        if self.id_picture > -1:    
            self.viewer.tag_lower(self.id_picture)
    # def get_items(self,x,y):
        # items =[]
        # if self.df_result is not None:
            # xy = (self.viewer.canvasx(xy[0]), self.viewer.canvasy(xy[1]))
            # #for key,val in self.editorItems.items():
            # #print(self.editorItems[(self.editorItems["profile"]==self.combo_profile.get())&(self.editorItems['camera']==int(self.combo_camera.get()))&(self.editorItems['editorItemId']>-1)])
            # for i,row in self.df_result[self.df_result['editorItemId']>-1].iterrows():
                # val = row['editorItemId']
                # coords = self.viewer.coords(val) #val must be INT32
                # #print("{}   {}   {}".format(row['name'],val,coords))
                # if self.in_region(xy,self.viewer.coords(val)):
                    # #print("Returned {}".format(val))
                    # items.append(val)            
    # return items   
    
    # def in_region(self,xy,coords):
        # #print("{} {}".format(xy,coords))
        # if (x>=coords[0] and y<=coords[2] and
            # xy[1]>=coords[1] and y<=coords[3]):
                # return True
        # else:
            # return False        
            
    def clear(self):
        if self.id_picture > -1:
            self.viewer.image = None
            self.viewer.delete(self.id_picture)