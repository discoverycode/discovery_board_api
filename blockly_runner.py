import os
from subprocess import check_output
import time


SCREEN_NAME = "DISCOVERY_RUNNER"

def run(filename):
    cmd = "screen -dmS " + SCREEN_NAME + " /usr/bin/python " + filename
    os.system(cmd)

def stop():
    cmd = "screen -X -S " + SCREEN_NAME + " quit"
    os.system(cmd)

def stop_all():
    os.system("killall screen")

def is_running():
    var = check_output(["screen -ls; true"],shell=True)
    if "." + SCREEN_NAME + "\t(" in var:
        return True
    else:
        return False

#e = Runner("/home/frazer/Downloads/DiscoveryServer/output/run.py")
#e.run()

#i = 0
#while e.is_running():
#    print("This is running")
#    i = i + 1
#    time.sleep(1.0)
#    if i > 10:
#        e.stop()
#	print("This has stopped")
