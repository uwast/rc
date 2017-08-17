#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32
from std_msgs.msg import Bool      
import time

tacking = False
position = 90


def callback(data):
    global tacking
    global position

    if not tacking:
        old_position = position
        pub = rospy.Publisher('rudder', Float32, queue_size=10)
        position_msg = Float32()
        position_msg.data = (90 - (60 * data.axes[0]))
        if abs(position_msg.data - old_position) > 5:
            pub.publish(position_msg)
            rospy.loginfo(rospy.get_caller_id() + " Read value: %f", data.axes[0])
            position = position_msg.data


def tacking_callback(tack):
    global tacking
    tacking = tack.data

    
def listener():
    rospy.init_node('joy_to_rudder', anonymous=True)
    rospy.Subscriber('joy', Joy, callback)
    rospy.Subscriber('tacking', Bool, tacking_callback)
    rospy.spin()
    

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
