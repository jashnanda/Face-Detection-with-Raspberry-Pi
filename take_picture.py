from picarx import Picarx
from vilib import Vilib
from pydoc import text
from time import sleep, time, strftime, localtime
import threading
import readchar
import os

px = Picarx()

def clamp_number(num, a, b):
    return max(min(num, max(a, b)), min(a, b))

def take_photo():
    _time = strftime('%Y-%m-%d-%H-%M-%S', localtime(time()))
    name = f'photo_{_time}'
    path = "photos/"
    Vilib.take_photo(name, path)
    print(f'photo saved as {path}{name}.jpg')

def main():
    Vilib.camera_start()
    Vilib.display()
    Vilib.face_detect_switch(True)
    x_angle = 0
    y_angle = 0

    while True:
        if Vilib.detect_obj_parameter['human_n'] != 0:
            take_photo()
            break
            

        #sleep(0.05)

if __name__ == "__main__":
    try:
        main()
    finally:
        px.stop()
        print("stop and exit")
        sleep(0.1)
