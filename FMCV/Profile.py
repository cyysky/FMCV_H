# #==========================================================================
# import hashlib
# from FMCV.peace import Peace,license
# lic = license()['Vision']
# if (hashlib.sha3_256((lic+lic).encode('utf-8')).hexdigest()!=Peace(lic)):
    # # https://stackoverflow.com/questions/9555133/e-printstacktrace-equivalent-in-python
    # #traceback.print_exc()
    # # https://stackoverflow.com/questions/73663/terminating-a-python-script
    # import os
    # import sys
    # os._exit(0)
    # sys.exit(0)
    # raise SystemExit  
    # 1/0      
    # pass
# #==========================================================================

import os
from os.path import join
import json
import traceback
import cv2
import copy
import base64
import numpy as np
from datetime import datetime, timezone

name = "default"

profile = []

loaded_profile = []

flag_save = False

def read(in_name):
    global profile, name
    name = in_name
    try:
        os.makedirs(join("Profile",name,"images"), exist_ok=True)        
        os.makedirs(join("Profile",name), exist_ok=True)
        with open(join("Profile",name,"profile.json"), "r") as f:
            profile = json.load(f)
        load()
    except:
        traceback.print_exc()
        
        profile = []
        
        profile.append([]) # src
        
        profile[0].append({"platform": {"x": 350, "y": 0, "z": 0, "roll": 0}, "roi": []})  # step
        
        # profile[0][0].append([]) # roi
        
        # profile[0][0][0].update({})
        
        print(json.dumps(profile , indent = 4))
        load()
        write()

def write():
    global profile, flag_save
    #print(loaded_profile)
    profile.clear()
    for src_n, src in enumerate(loaded_profile):
        profile.append([])
        for step_n, step in enumerate(src):
            #
            profile[src_n].append([])
            profile[src_n][step_n] = {}
            profile[src_n][step_n]["platform"] = step["platform"]
            profile[src_n][step_n]["roi"] = []
            for roi_n, roi in enumerate(step["roi"]):
                #print(self.Util.without_keys(roi,{"img"})) #debug use
                profile[src_n][step_n]["roi"].append(self.Util.without_keys(roi,{"img"}))
                #if roi.get('img') is not None:
                #    profile[src_n][step_n][roi_n].update({"image":base64.b64encode(cv2.imencode('.png',roi['img'])[1]).decode()})
                
    file_name = self.Util.utc_to_local(datetime.utcnow()).strftime('%Y-%m-%d_%H%M%S_%f')[:-3] + "_profile.json"
    try :
        os.makedirs(join("Profile",name,"Profile_Backup"), exist_ok=True)     
        os.replace(join("Profile",name,"profile.json"),join("Profile",name,"Profile_Backup",file_name))
    except:
        print("no rename needed")
    with open(join("Profile",name,"profile.json"), "w") as outfile:
        outfile.write(json.dumps(profile , indent = 4))
        print(join("Profile",name,"profile.json"))
        flag_save = False
        
def load():
    global profile, loaded_profile, name

    loaded_profile.clear()
    loaded_profile
    for src_n, src in enumerate(profile):
        loaded_profile.append([])
        for step_n, step in enumerate(src):
            loaded_profile[src_n].append([])
            # print("Step:")
            # print(json.dumps(step["platform"], indent=4))
            # # extract platform param
            # loaded_profile[src_n][step_n] = step["platform"]
            loaded_profile[src_n][step_n] = {}
            loaded_profile[src_n][step_n]["platform"] = step["platform"]
            loaded_profile[src_n][step_n]["roi"] = []
            for roi_n, roi in enumerate(step["roi"]):
                # each step include platform position and multiple ROIs
                loaded_profile[src_n][step_n]["roi"].append(roi)
                #print(json.dumps(roi, indent=4))
                if roi.get('image') is not None:
                    loaded_profile[src_n][step_n]["roi"][roi_n].update({"img":cv2.imdecode(np.frombuffer(base64.b64decode(roi["image"]), dtype=np.uint8),flags=cv2.IMREAD_COLOR)})

def add_source(src_n):
    print(src_n)
    global loaded_profile
    loaded_profile.insert(src_n + 1, [])
    loaded_profile[src_n + 1].append([])
    
def remove_source(src_n):
    global loaded_profile
    loaded_profile.pop(src_n)

def add_step(src_n, step_n):
    print(step_n)
    global loaded_profile
    loaded_profile[src_n].insert(step_n + 1, {"platform": {"x": 350, "y": 0, "z": 0, "roll": 0}, "roi": []})
    
def insert_step(src_n, step_n):
    print(step_n)
    global loaded_profile
    loaded_profile[src_n].insert(step_n-1, {"platform": {"x": 350, "y": 0, "z": 0, "roll": 0}, "roi": []})
    
def remove_step(src_n, step_n):
    global loaded_profile
    loaded_profile[src_n].pop(step_n)
    
def add_roi(src_n, step_n,roi_n,roi):
    global loaded_profile
    loaded_profile[src_n][step_n]["roi"].insert(roi_n+1,roi)

def update_roi(src_n, step_n, roi_n, roi):
    global loaded_profile
    loaded_profile[src_n][step_n]["roi"][roi_n].update(roi)
    
def remove_roi(src_n, step_n,roi_n):
    global loaded_profile
    loaded_profile[src_n][step_n]["roi"].pop(roi_n)

def update_roi(src_n, step_n,roi_n,pair):
    global loaded_profile
    loaded_profile[src_n][step_n]["roi"][roi_n].update(pair)

def init(s):
    global self
    self = s 

def write_image(image_folder_name, cropped):
    file_name = self.Util.utc_to_local(datetime.utcnow()).strftime('%Y-%m-%d_%H%M%S_%f')[:-3]
    cv2.imwrite(join("Profile", name, "images", image_folder_name, file_name+".png"), cropped)
    return join("Profile", name, "images", image_folder_name, file_name+".png")

def create_image_folder(image_folder_name):
    os.makedirs(join("Profile",name,"images",image_folder_name), exist_ok=True)
    
def get_image_folders_list():
    return next(os.walk(join("Profile",name,"images")))[1]
    
def get_image_folder_path(folder_name):
    os.makedirs(join("Profile",name,"images",folder_name), exist_ok=True)
    return join("Profile",name,"images",folder_name)
    