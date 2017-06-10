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
wind_dir = 0

def callback(data):
    global cancel
    global tacking_direction
    global pub1
    global pub
    global position
    global wind_dir

    if data.buttons[0] and tacking_direction == 0: #x is pressed
        rospy.loginfo(rospy.get_caller_id() + "Tack requested.")
	if wind_dir <180:
	    pub.publish(30.0)
	    position = 30.0
	    tacking_direction = -1
	else:
	    pub.publish(150.0)
	    position = 150.0
	    tacking_direction = 1
	
	pub1.publish(True)
    
    elif data.buttons[2] and not tacking_direction == 0:
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
    global cancel
    global tacking_direction
    global position
    global wind_dir

    rate = rospy.Rate(100)
    position_msg = Float32()
    wind_dir = direction.data

    if tacking_direction == 1:
        if direction.data > 150:
            if not position == 150.0:
                position_msg.data = 150.0
		position = position_msg.data
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
                position = position_msg.data
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
