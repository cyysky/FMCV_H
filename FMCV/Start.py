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

#https://stackoverflow.com/questions/1676835/how-to-get-a-reference-to-a-module-inside-the-module-itself
import sys
self = sys.modules[__name__]

from FMCV import Util
from FMCV import Cv
from FMCV import Config
Config.init(self)

from FMCV import Profile
Profile.init(self)
Profile.read(Config.config["PROFILE"]["name"])

from FMCV import Process
Process.init(self)

from FMCV.Ai import CNN
CNN.init(self)
CNN.load()

from FMCV.Ui import ActionUi
ActionUi.init(self)

from FMCV.Ui import MainUi
MainUi.init(self)
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

os.environ["CUDA_VISIBLE_DEVICES"] = Config.config["CUDA"]["CUDA_VISIBLE_DEVICES"]

def run():
    Main.update_view()
    MainUi.top.mainloop()