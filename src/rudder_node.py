#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32
from std_msgs.msg import Bool      
import time

tacking = False  # Whether or not we are tacking
rudder_pos = 90  # What the rudder position is (0-180)
pub = rospy.Publisher('rudder', Float32, queue_size=10)


def joy_callback(controller):
    global tacking
    global rudder_pos
    global pub

    if not tacking:
        # If the boat is not currently tacking, then setup a message to send to the /rudder topic
        rudder_pos_old = rudder_pos
        position_msg = Float32()

        # Set the rudder position to be a min of 30 and max of 150
        position_msg.data = (90 - (60 * controller.axes[0]))

        # Only publish if the change in rudder angle is greater than 5
        if abs(position_msg.data - rudder_pos_old) > 5:
            pub.publish(position_msg)
            rospy.loginfo(rospy.get_caller_id() + " Read value: %f", data.axes[0])
            rudder_pos = position_msg.data


def tacking_callback(tack):
    # If tacking topic changes, update the tacking global variable to reflect that change
    global tacking
    tacking = tack.data

    
def listener():
    # Setup subscribers
    rospy.init_node('joy_to_rudder', anonymous=True)
    rospy.Subscriber('joy', Joy, joy_callback)
    rospy.Subscriber('tacking', Bool, tacking_callback)
    rospy.spin()
    

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
