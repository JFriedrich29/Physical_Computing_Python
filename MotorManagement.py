from CameraHandler import *
import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825

def execute(x, y):
    killgphoto2Process()
    createSaveFolder()
    Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
    Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))    
    Motor1.SetMicroStep('softward','1/32step')
    Motor2.SetMicroStep('softward','1/32step')
    Motor1.Stop()
    Motor2.Stop()
        
    captureImage()
    renameFiles()
    for j in range(x-1):
        Motor1.TurnStep(Dir='forward', steps=200*20//x, stepdelay=0.002)
        Motor1.Stop()
        time.sleep(1)
        for k in range(y):
            captureImage()
            renameFiles()
            Motor2.TurnStep(Dir='forward', steps=200*40//y, stepdelay = 0.002)
            Motor2.Stop()
            time.sleep(1)
        
    Motor1.TurnStep(Dir='forward', steps=200*20//x, stepdelay=0.002)
    Motor1.Stop()
    time.sleep(1)
    captureImage()
    renameFiles()
    
    Motor1.TurnStep(Dir='backwards', steps=200*20, stepdelay=0.002)
    Motor1.Stop()
    time.sleep(1)
            