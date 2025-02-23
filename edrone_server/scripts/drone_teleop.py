#!/usr/bin/env python
import rospy
from edrone_client.msg import *

from geometry_msgs.msg import Twist

import sys, select, termios, tty

msg = """
Control Your eDrone!
---------------------------
Moving around:
   u    i    o
   j    k    l
        m     


a : Arm drone
d : Dis-arm drone
w : Increase Altitude
s : Increase Altitude
u,o: Change Yaw

CTRL-C to quit
"""

KeyBinding = {
       #key:(roll,pitch,yaw,throt,aux1,aux2,aux3,aux4)
        'i':(1500,1900,1500,1500,1500,1500,1500,1500),
        'a':(1500,1500,1500,1000,1500,1500,1500,1500),
        'j':(1900,1500,1500,1500,1500,1500,1500,1500),
        'l':(1100,1500,1500,1500,1500,1500,1500,1500),
        'd':(1500,1500,1500,1300,1500,1500,1500,1200),
        'm':(1500,1100,1500,1500,1500,1500,1500,1500),
        'w':(1500,1500,1500,1900,1500,1500,1500,1500),
        's':(1500,1500,1500,1100,1500,1500,1500,1500),
        'o':(1500,1500,1600,1900,1500,1500,1500,1500),
        'u':(1500,1500,1400,1100,1500,1500,1500,1500),
           }

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

speed = .2
turn = 1

def vels(speed,turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    
    rospy.init_node('eDrone_teleop')
    pub = rospy.Publisher('/drone_command', edrone_msgs, queue_size=5)

    roll = 1500
    pitch = 1500
    yaw = 1500
    throttle = 1500
    aux1=1500
    aux2=1500
    aux3=1500
    aux4=1500
    count =0

    try:
        print(msg)
        while(1):
            key = getKey()
            if key in KeyBinding.keys():
                roll = KeyBinding[key][0]
                pitch = KeyBinding[key][1]
                yaw = KeyBinding[key][2]
                throttle = KeyBinding[key][3]
                aux1=KeyBinding[key][4]
                aux2=KeyBinding[key][5]
                aux3=KeyBinding[key][6]
                aux4=KeyBinding[key][7]
                count = 0
            if (key == '\x03'):
                break
            else:
                count = count + 1
                if count > 4:
                    roll = 1500
                    pitch = 1500
                    yaw = 1500
                    throttle = 1500
                    aux1=1500
                    aux2=1500
                    aux3=1500
                    aux4=1500

            cmd = edrone_msgs()
            cmd.rcRoll = roll; cmd.rcPitch = pitch; cmd.rcYaw = yaw
            cmd.rcThrottle = throttle; cmd.rcAUX1 = aux1; cmd.rcAUX2 = aux2
            cmd.rcAUX3 = aux3; cmd.rcAUX4 = aux4
            pub.publish(cmd)

    except Exception as e:
        print(e)

    finally:
        cmd = edrone_msgs()
        cmd.rcRoll = roll; cmd.rcPitch = pitch; cmd.rcYaw = yaw
        cmd.rcThrottle = throttle; cmd.rcAUX1 = aux1; cmd.rcAUX2 = aux2
        cmd.rcAUX3 = aux3; cmd.rcAUX4 = aux4
        pub.publish(cmd)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

