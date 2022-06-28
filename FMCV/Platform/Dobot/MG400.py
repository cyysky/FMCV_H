from FMCV.Platform.PlatformInterface import PlatformInterface
#from FMCV.Platform.Dobot.dobot_api import DobotApiDashboard, DobotApi, DobotApiMove
from FMCV.Platform.Dobot.dobot_api import *
from FMCV.Platform.Dobot.alarm_controller import alarm_controller_list
from FMCV.Platform.Dobot.alarm_servo import alarm_servo_list
import numpy as np
from threading import Thread
import time
import json
import traceback

class MG400(PlatformInterface):
    """Inherit from PlatformInterface"""

    # actual cartesian position
    actual_x = 0
    actual_y = 0
    actual_z = 0
    actual_roll = 0

    MODE_LOOKUP = {
        1: "MODE_INIT",
        2: "MODE_BRAKE_OPEN",
        3: "",
        4: "MODE_DISABLED",
        5: "MODE_ENABLE",
        6: "MODE_BACKDRIVE",
        7: "MODE_RUNNING",
        8: "MODE_RECORDING",
        9: "MODE_ERROR",
        10: "MODE_PAUSE",
        11: "MODE_JOG"
    }

    def __init__(self, feedback_callback=None):
        self.is_connected = False

        self.ipaddr = "192.168.1.6"     # default ip
        self.dashboard_port = "29999"
        self.move_port = "30003"
        #self.feedback_port = "30004"   # feedback rate ~8ms for port 30004
        self.feedback_port = "30005"    # feedback rate ~200ms for port 30005
        self.text_log = ""
        self.mode = ""
        self.is_error_occur = False

        self.alarm_controller_dict = self.convert_dict(alarm_controller_list)
        self.alarm_servo_dict = self.convert_dict(alarm_servo_list)

        if(feedback_callback is not None):
            self.feedback_callback = feedback_callback

    def model_name(self):
        return "Dobot MG400"

    def operating_mode(self):
        return self.mode

    def is_error(self):
        return self.is_error_occur

    def get_log(self):
        return self.text_log

    def x(self):
        return self.actual_x

    def y(self):
        return self.actual_y

    def z(self):
        return self.actual_z

    def roll(self):
        return self.actual_roll

    def connect(self, ipaddress=""):
        if(self.is_connected == False):
            try:
                self.ipaddr = ipaddress
                self.client_dash = DobotApiDashboard(
                    self.ipaddr, int(self.dashboard_port), self.text_log)
                self.client_move = DobotApiMove(
                    self.ipaddr, int(self.move_port), self.text_log)
                self.client_feed = DobotApi(
                    self.ipaddr, int(self.feedback_port), self.text_log)

                self.is_connected = True

                # start feedback thread
                self.feedback_thread = Thread(target=self.feedback)
                self.feedback_thread.setDaemon(True)
                self.feedback_thread.start()

                print("MG400 Connected")

            except Exception as e:
                print(f"Connection Error: {e}")

                self.is_connected = False
        return self.is_connected


    def disconnect(self):
        try:
            if (self.is_connected == True):
                #print("MG400 Disconnecting...")
                self.is_connected = False       # set to false 1st to break the loop in feedback thread
                time.sleep(0.1)
                #if(self.feedback_thread is not None):
                    #self.feedback_thread.join()     # stop the feedback thread

                self.client_dash.close()
                self.client_feed.close()
                self.client_move.close()
                self.client_dash = None
                self.client_feed = None
                self.client_move = None
                print("MG400 Disconnected")
        except:
            traceback.print_exc()
        return self.is_connected

    def enable_platform(self) -> bool:
        self.client_dash.EnableRobot()
        return True

    def disable_platform(self) -> bool:
        self.client_dash.DisableRobot()
        return True

    def clear_error(self) -> bool:
        self.client_dash.ClearError()
        return True

    def reset(self) -> bool:
        self.client_dash.ResetRobot()
        return True

    def move_to_home_async(self, complete_callback):
        # do the works here
        complete_callback()

    def move_to_point_async(self, x=0, y=0, z=0, roll=0, complete_callback=None):
        # do the works here
        self.client_move.MovJ(float(x),
                              float(y),
                              float(z),
                              float(roll))
        #TODO: create another thread to get the feed back
        if(complete_callback is not None):
            complete_callback()

    def convert_dict(self, alarm_list):
        alarm_dict = {}
        for i in alarm_list:
            alarm_dict[i["id"]] = i
        return alarm_dict

    def feedback(self):
        try:
            hasRead = 0
            while True:
                if not self.is_connected:
                    #print("Stop feedback thread")
                    break

                data = bytes()
                while hasRead < 1440:
                    temp = self.client_feed.socket_dobot.recv(1440 - hasRead)
                    if len(temp) > 0:
                        hasRead += len(temp)
                        data += temp
                hasRead = 0

                a = np.frombuffer(data, dtype=MyType)
                #print("robot_mode:", a["robot_mode"][0])
                #print("test_value:", hex((a['test_value'][0])))
                if hex((a['test_value'][0])) == '0x123456789abcdef':
                    # print('tool_vector_actual',
                    #       np.around(a['tool_vector_actual'], decimals=4))
                    # print('q_actual', np.around(a['q_actual'], decimals=4))

                    # Refresh Properties
                    self.speec_scaling = a["speed_scaling"][0]
                    self.mode = self.MODE_LOOKUP[a["robot_mode"][0]]

                    self.di_input = bin(a["digital_input_bits"][0])[2:].rjust(64, '0')
                    self.di_output = bin(a["digital_output_bits"][0])[2:].rjust(64, '0')

                    # Refresh coordinate points
                    self.actual_feed_joint = a["q_actual"]
                    self.coord_feed_joint = a["tool_vector_actual"]
                    self.actual_x = self.coord_feed_joint[0][0]
                    self.actual_y = self.coord_feed_joint[0][1]
                    self.actual_z = self.coord_feed_joint[0][2]
                    self.actual_roll = self.coord_feed_joint[0][3]

                    # check alarms
                    if a["robot_mode"] == 9:
                        self.is_error_occur = True
                        self.display_error_info()
                    else:
                        self.text_log = ""
                        self.is_error_occur = False
                feedback_data = {}
                if((self.feedback_callback is not None) and (self.is_connected)):
                    self.feedback_callback(feedback_data)

                time.sleep(0.005)
        except:
            pass
        finally:
            #print("Feedback thread ended")
            pass

    def display_error_info(self):
        error_list = self.client_dash.GetErrorID().split("{")[1].split("}")[0]
        print(error_list)
        error_list = json.loads(error_list)
        print("error_list:", error_list)
        if error_list[0]:
            for i in error_list[0]:
                self.form_error(i, self.alarm_controller_dict, "Controller Error")

        for m in range(1, len(error_list)):
            if error_list[m]:
                for n in range(len(error_list[m])):
                    self.form_error(n, self.alarm_servo_dict, "Servo Error")

    def form_error(self, index, alarm_dict: dict, type_text):
        if index in alarm_dict.keys():
            date = datetime.datetime.now().strftime("%Y.%m.%d:%H:%M:%S ")
            error_info = f"Time Stamp:{date}\n"
            error_info = error_info + f"ID:{index}\n"
            error_info = error_info + \
                         f"Type:{type_text}\nLevel:{alarm_dict[index]['level']}\n" + \
                         f"Solution:{alarm_dict[index]['en']['solution']}\n"

            print(error_info)
            self.text_log = error_info

