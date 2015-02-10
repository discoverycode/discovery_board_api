import os
import time
import discovery_bot

# Init the classes
robot = discovery_bot.Movement()

robot.forward()
time.sleep(1)
robot.stop()