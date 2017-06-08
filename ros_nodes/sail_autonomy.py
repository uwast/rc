#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Bool
      
import time
request = "Manual"
autonomy = False

def callback(data):
    global request
    global autonomy
    rate = rospy.Rate(100)

    if data.buttons[5] == 1 and data.buttons[4] == 0:
        request = "Autonomy"
        autonomy = True
    elif data.buttons[5] == 0 and data.buttons[4] == 1:
        request = "Manual"
        autonomy = False

    rospy.loginfo(rospy.get_caller_id() + " Autonomy Request: %s", request)
    global pub
    pub = rospy.Publisher('autonomy', Bool, queue_size=10)

    pub.publish(autonomy)
    rate.sleep()

def listener():
    rospy.init_node('autonomy', anonymous=True)
    rospy.Subscriber('joy', Joy, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
