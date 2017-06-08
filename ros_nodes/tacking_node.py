#!/usr/bin/env python
import rospy
import roslaunch
from sensor_msgs.msg import Joy
from std_msgs.msg import Int32
from std_msgs.msg import Bool
from std_msgs.msg import Float32
import time

cancel = False
tacking = False
wind_dir = 180

def callback(data):
    global cancel
    global tacking

    if data.buttons[0] and not tacking: #x is pressed
        tack()
        tacking = True
        rospy.loginfo(rospy.get_caller_id() + "Tack requested.")

    elif data.buttons[2] and not cancel and tacking:
        cancel = True
        rospy.loginfo(rospy.get_caller_id() + "Tack cancelled")


def tack():
    global pub1
    pub1 = rospy.Publisher('tacking', Bool, queue_size=10)
    pub1.publish(True)

    global cancel
    global wind_dir
    global pub
    pub = rospy.Publisher('rudder', Float32, queue_size=10)
    rate = rospy.Rate(100)

    if(wind_dir > 180 and not cancel):
        while(wind_dir>150):
            position_msg = Float32()
            position_msg.data = 150.0
            pub.publish(position_msg)
            rate.sleep()
            #rospy.spinOnce()

    else:
        while(wind_dir<210 and not cancel):
            position_msg = Float32()
            position_msg.data = 30.0
            pub.publish(position_msg)
            rate.sleep()
            #rospy.spinOnce()

    position_msg = Float32()
    position_msg.data = 90.0
    pub1.publish(False)

def callback_wind(direction):
    global wind_dir
    wind_dir = direction.data



def listener():
    rospy.init_node('joy_to_tack', anonymous=True)
    rospy.Subscriber('joy', Joy, callback)
    rospy.Subscriber('anemometer', Int32, callback_wind)
    rospy.spin()


if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
