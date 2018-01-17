#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Bool
      
import time
request = "Manual"
autonomy = False
pub = rospy.Publisher('autonomy', Bool, queue_size=10)


def joy_callback(controller):
    global request
    global autonomy
    global pub
    rate = rospy.Rate(100)
  
    # If R1 is pushed and L1 is not then set autonomous mode
    if controller.buttons[5] == 1 and controller.buttons[4] == 0:
        request = "Autonomy"
        autonomy = True
    # If L1 is pushed and R1 is not then set manual mode
    elif controller.buttons[5] == 0 and controller.buttons[4] == 1:
        request = "Manual"
        autonomy = False

    rospy.loginfo(rospy.get_caller_id() + " Autonomy Request: %s", request)
    pub.publish(autonomy)
    rate.sleep()

def listener():
    # Setup subscribers
    rospy.init_node('autonomy', anonymous=True)
    rospy.Subscriber('joy', Joy, joy_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
