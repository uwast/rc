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
pub = rospy.Publisher('winch', Int32, queue_size=10)


def callback(data):
    global position
    global request
    global autonomy
    global pub

    rate = rospy.Rate(100)

    if autonomy is False:
        if data.axes[6] < 0:
            request = "Broad"
            position = 1500  # 1.5 turns
        elif data.axes[6] > 0:
            request = "Beam"
            position = 1100  # Three turns
        elif data.axes[7] < 0:
            request = "Run"
            position = 1600  # Fully out
        elif data.axes[7] > 0:
            request = "Close"
            position = 0  # Five Turns
        else:
            request = "Hold"

    rate.sleep()


def callback_autonomy(setting):
    global autonomy
    autonomy = setting.data
    rospy.loginfo(rospy.get_caller_id() + " Autonomy Mode: %r", autonomy)


def callback_wind(direction):
    global position
    global autonomy
    global wind_dir
    global pub

    wind_dir = direction.data
    rate = rospy.Rate(100)

    if autonomy is True:
        if wind_dir < (180 + max_angle) and wind_dir > (180 - max_angle):
            new_position = 0
        elif wind_dir >= (180 - max_angle):
           new_position = (600 / (180 - max_angle)) * abs(wind_dir-(max_angle + 180)) + 1000
        else:
            new_position = (600 / (180 - max_angle)) * abs(wind_dir-(180 - max_angle)) + 1000
        if abs(new_position - position) > 5:
            position = new_position
            pub.publish(position)
            rospy.loginfo(rospy.get_caller_id() + " Autonomy Request: %f", position)

    rate.sleep()


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
