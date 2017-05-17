#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Int32
from std_msgs.msg import Bool
      
import time

autonomy = False
wind_dir = 0
request = "Hold"
position = 0
max_angle = 30

def callback(data):
    global position
    global request
    global autonomy

    if autonomy is False:
        if data.axes[6] < 0:
            request = "Broad"
            position = 540  # 1.5 turns
        elif data.axes[6] > 0:
            request = "Beam"
            position = 1080  # Three turns
        elif data.axes[7] < 0:
            request = "Run"
            position = 0  # Fully out
        elif data.axes[7] > 0:
            request = "Close"
            position = 1800  # Five Turns
        else:
            request = "Hold"

    rospy.loginfo(rospy.get_caller_id() + " Controller Request: %s", request)
    global pub
    pub = rospy.Publisher('winch', Int32, queue_size=10)
    pub.publish(position)

def callback_autonomy(setting):
    global autonomy
    autonomy = setting.data
    rospy.loginfo(rospy.get_caller_id() + " Autonomy Mode: %r", autonomy)

def callback_wind(direction):
    global position
    global autonomy
    global wind_dir
    wind_dir = direction.data

    if autonomy is True:
        if wind_dir < max_angle or wind_dir > (360 - max_angle):
            position = 1800  # Five turns, close hauled
        elif wind_dir >= 180:

            position = (1800 / (180 - max_angle)) * (wind_dir - 180)
        else:
            position = 1800 - ((1800 / (180 - max_angle)) * (wind_dir-max_angle))

    rospy.loginfo(rospy.get_caller_id() + " Autonomy Request: %f", position)
    global pub
    pub = rospy.Publisher('winch', Int32, queue_size=10)
    pub.publish(position)

def listener():
    rospy.init_node('joy_to_winch', anonymous=True)
    rospy.Subscriber('joy', Joy, callback)
    rospy.Subscriber('autonomy', Bool, callback_autonomy)
    rospy.Subscriber('anemometer', Int32, callback_wind)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
