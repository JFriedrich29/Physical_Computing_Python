from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess

save_loc = "/home/pi/Desktop/gphoto/Images/" + datetime.now().strftime("%Y-%m-%d")

def killgphoto2Process():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)
  
def createSaveFolder():
    try:
        os.makedirs(save_loc)
    except:
        print("Folder already exists")
    os.chdir(save_loc)
  
def captureImage():
    gp(["--capture-image-and-download"])
    
    
def renameFiles():
    for filename in os.listdir("."):
        if len(filename) <20:
            if filename.endswith(".jpg"):
                os.rename(filename, datetime.now().strftime("%Y-%m-%d %H:%M:%S")+".jpg")
    
    