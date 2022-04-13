import webbrowser

def init(s):
    global self
    self = s 
    
def cnn_train():
    self.CNN.train()
   
def save_profile():
    self.Profile.write()
    
def go_next():
    print("Robot Next Step")
    self.Com.go_next()
    print("Skip Step")
    #self.Main.next_step()
    self.Main.detect(self.Main.detected_step+1)
    refresh_main_ui()



def skip_step():
    print("Skip Step")
    self.Main.next_step()
    refresh_main_ui()
    
def detect():
    print("detect by step")
    print("cmb.current() {} detected_step{}".format(self.MainUi.cmb.current(),self.Main.detected_step))
    self.Main.detect()
    refresh_main_ui()
    self.MainUi.write('Current Detection Step is {}'.format(self.Main.detected_step))
    
    
def detect_current_step():
    print("detect current step")
    print("cmb.current() {} detected_step{}".format(self.MainUi.cmb.current(),self.Main.detected_step))
    self.Main.detect(self.MainUi.cmb.current())
    refresh_main_ui()
    self.MainUi.write('Current Detection Step is {}'.format(self.Main.detected_step))

def reset_detection_step():
    self.Main.reset()
    refresh_main_ui()
    
def open_folder(folder_name):
    pth = self.Profile.get_image_folder_path(folder_name)
    webbrowser.open(pth)
    
def refresh_main_ui():
    self.MainUi.steps_lbl.config(text = "Steps = {}".format(self.Main.detected_step + 1))
    self.MainUi.cmb.current(self.Main.detected_step)
    self.MainUi.cmb_pos = self.Main.detected_step
    self.MainUi_Refresh.refresh_listbox(self.Main.detected_step)
    self.MainUi_Refresh.refresh_result_view(self.Main.detected_step)
    self.MainUi.frm_cams.update_results()