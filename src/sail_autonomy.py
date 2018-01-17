#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Bool
from boat_nav.msg import BoatState

state = 0
      
import time
pub = rospy.Publisher('boat_state', BoatState, queue_size=10)


def state_callback(new_state):
    global state
    state = new_state



def joy_callback(controller):
    global pub
    global state
    rate = rospy.Rate(10)

    # If R1 is pushed and L1 is not the set autonomous mode

    if controller.buttons[5] == 1 and controller.buttons[4] == 0:
        state.major = BoatState.MAJ_AUTONOMOUS
    # If L1 is pushed and R1 is not then set manual mode
    elif controller.buttons[5] == 0 and controller.buttons[4] == 1:
        state.major = BoatState.MAJ_RC

    pub.publish(state)
    rate.sleep()

def listener():
    # Setup subscribers
    rospy.init_node('rc_auto_node', anonymous=True)
    rospy.Subscriber('joy', Joy, joy_callback)
    rospy.Subscriber('boat_state', BoatState, state_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
