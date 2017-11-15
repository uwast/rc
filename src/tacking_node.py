#!/usr/bin/env python
import rospy
import roslaunch
from sensor_msgs.msg import Joy
from std_msgs.msg import Int32
from std_msgs.msg import Bool
from std_msgs.msg import Float32
import time

tack_request = False
tacking_direction = 0
pub_tacking = rospy.Publisher('tacking', Bool, queue_size=10)
pub_rudder = rospy.Publisher('rudder', Float32, queue_size=10)
rudder_pos = 90.0
wind_dir = 0

def callback(controller):
    global tacking_direction
    global pub_tacking
    global pub_rudder
    global rudder_pos
    global wind_dir

    # x is pressed then request a tack
    if controller.buttons[0] and tacking_direction == 0:
        rospy.loginfo(rospy.get_caller_id() + "Tack requested.")

        # If a tack is requested, figure out which side we are tacking and set the rudder accordingly
        if wind_dir < 180:
            pub_rudder.publish(30.0)
            rudder_pos = 30.0
            tacking_direction = -1
        else:
            pub_rudder.publish(150.0)
            rudder_pos = 150.0
            tacking_direction = 1

        pub_tacking.publish(True)

    # o is pressed, therefore cancelling a previously requested tack
    elif controller.buttons[2] and not tacking_direction == 0:
        # Reset rudder and change tacking state
        tacking_direction = 0
        rospy.loginfo(rospy.get_caller_id() + "Tack cancelled")
        rudder_pos_msg = Float32()
        rudder_pos_msg.data = 90.0
        pub_rudder.publish(rudder_pos_msg)
        pub_tacking.publish(False)
        rudder_pos = rudder_pos_msg.data


def anemometer_callback(wind_direction):
    global pub_tacking
    global pub_rudder
    global tacking_direction
    global rudder_pos
    global wind_dir

    rate = rospy.Rate(10)
    rudder_pos_msg = Float32()
    wind_dir = wind_direction.data

    # Based on direction of tack, keep the rudder turned while the boat crosses wind and passes 30 degrees to the
    # other side, then set the rudder back to 90
    if tacking_direction == 1:
        if direction.data > 150:
            if not rudder_pos == 150.0:
                rudder_pos_msg.data = 150.0
                rudder_pos = rudder_pos_msg.data
                pub_rudder.publish(rudder_pos_msg)
            rate.sleep()
        else:
            tacking_direction = 0
            rudder_pos_msg.data = 90.0
            pub_rudder.publish(rudder_pos_msg)
            pub_tacking.publish(False)

    elif tacking_direction == -1:
        if direction.data < 210:
            if not rudder_pos == 30.0:
                rudder_pos_msg.data = 30.0
                rudder_pos = rudder_pos_msg.data
                pub_rudder.publish(rudder_pos_msg)
            rate.sleep()
        else:
            tacking_direction = 0
            rudder_pos_msg.data = 90.0
            pub_rudder.publish(rudder_pos_msg)
            pub_tacking.publish(False)

    rate.sleep()


def listener():
    rospy.init_node('joy_to_tack', anonymous=True)
    rospy.Subscriber('joy', Joy, joy_callback)
    rospy.Subscriber('anemometer', Int32, anemometer_callback)
    rospy.spin()


if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
