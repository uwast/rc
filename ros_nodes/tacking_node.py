#!/usr/bin/env python
import rospy
import roslaunch
from sensor_msgs.msg import Joy
from std_msgs.msg import Int32
from std_msgs.msg import Bool
from std_msgs.msg import Float32
import time

cancel = False
tack_request = False
tacking_direction = 0
pub1 = rospy.Publisher('tacking', Bool, queue_size=10)
pub = rospy.Publisher('rudder', Float32, queue_size=10)
position = 90.0

def callback(data):
    global cancel
    global tack_request
    global tacking_direction
    global pub1
    global pub
    global position

    if data.buttons[0] and not tack_request and tacking_direction == 0: #x is pressed
        tack_request = True
        rospy.loginfo(rospy.get_caller_id() + "Tack requested.")

    elif data.buttons[2] and (tack_request or not tacking_direction == 0):
        tack_request = False
        tacking_direction = 0
        rospy.loginfo(rospy.get_caller_id() + "Tack cancelled")
        position_msg = Float32()
        position_msg.data = 90.0
        pub.publish(position_msg)
        pub1.publish(False)
        position = position_msg.data


def callback_wind(direction):
    global pub1
    global pub
    global tack_request
    global cancel
    global tacking_direction
    global position

    rate = rospy.Rate(100)
    position_msg = Float32()

    if tack_request:
        if direction.data > 180:
            tacking_direction = 1
            position_msg.data = 150.0

        else:
            tacking_direction = -1
            position_msg.data = 30.0

        tack_request = False
        pub.publish(position_msg)
        rate.sleep()
        pub1.publish(True)
        position = position_msg.data

    elif tacking_direction == 1:
        if direction.data > 150:
            if not position == 150.0:
                position_msg.data = 150.0
                pub.publish(position_msg)
            rate.sleep()
        else:
            tacking_direction = 0
            position_msg.data = 90.0
            pub.publish(position_msg)
            pub1.publish(False)

    elif tacking_direction == -1:
        if direction.data < 210:
            if not position == 30.0:
                position_msg.data = 30.0
                pub.publish(position_msg)
            rate.sleep()
        else:
            tacking_direction = 0
            position_msg.data = 90.0
            pub.publish(position_msg)
            pub1.publish(False)

    rate.sleep()


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
