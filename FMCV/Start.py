import os

#https://stackoverflow.com/questions/1676835/how-to-get-a-reference-to-a-module-inside-the-module-itself
import sys
self = sys.modules[__name__]

#Command line control
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-p","--profile", help="Specific A profile to start with", default = None)
args = parser.parse_args()

#Start FMCV Module

from FMCV import Util
from FMCV import Cv
from FMCV import Config
Config.init(self)

from FMCV import Profile
Profile.init(self)

from FMCV import Process
Process.init(self)

from FMCV.Ai import CNN
CNN.init(self)

from FMCV.Ui import ActionUi
ActionUi.init(self)

from FMCV.Ui import MainUi
MainUi.init(self)
# Some legacy code here, some later added module already using object base tkinter widgets
from FMCV.Ui import MainUi_Aux 
from FMCV.Ui import MainUi_Edit 
from FMCV.Ui import MainUi_Refresh 
from FMCV.Ui import MainUi_Results 
    
from FMCV.Ui import EditorUi
EditorUi.init(self)

from FMCV import Main
Main.init(self)
Main.reset()

Serial = None
ModbusTCP = None

from FMCV import Com
Com.init(self)

from FMCV import Log
Log.init(self)
    
Camera = None
exec("from FMCV.Camera import {} as Camera".format(Config.config['CAMERA']['name']))

from FMCV.Platform.Platform import Platform, CartesianPosition
MovingPlatform = None
Main.init_moving_platform()

os.environ["CUDA_VISIBLE_DEVICES"] = Config.config["CUDA"]["CUDA_VISIBLE_DEVICES"]

def run():
    Main.update_view()
    MainUi.top.mainloop()