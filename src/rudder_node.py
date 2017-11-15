#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32
from std_msgs.msg import Bool
from boat_nav.msg import BoatState
import time

# Declare global variables needed for the node
rudder_pos = 90  # What the rudder position is (0-180)
cur_boat_heading = 0
wind_heading = 0
state = 0

# Declare the publishers for the node
rudder_pos_pub = rospy.Publisher('rudder', Float32, queue_size=10)
boat_state_pub = rospy.Publisher('boat_state', BoatState, queue_size=10)


# If the boat state topic changes, update local boat state
def boat_state_callback(new_state):
	global state
	state = new_state
	
	
# If the wind heading topic changes, update local wind heading
def wind_callback(heading):
	global wind_heading
	wind_heading = heading
	
	
# If the boat heading topic changes, update rudder PID setpoint
def heading_callback(target_heading):
	global wind_heading
	global state
	global cur_boat_heading
	
	# Perhaps a worthwhile check, but not really super important because this callback will never be called if these conditions are not met in path_planning_node
	if state.major is not BoatState.MAJ_AUTONOMOUS or state.minor is not BoatState.MIN_PLANNING:
		return
	
	# We have a new valid setpoint, therefore output it	
	rospy.loginfo(rospy.get_caller_id() + " New rudder setpoint: %f", target_heading)

	# If the current heading and the new heading are on opposite sides of the wind, we need to tack
    # HOW DO WE HANDLE 0-360 JUMP
	if (target_heading < wind_heading and cur_boat_heading > wind_heading) or (target_heading > wind_heading and cur_boat_heading < wind_heading):
		state.minor = BoatState.MIN_TACKING
		boat_state_pub.publish(state)
		rospy.loginfo(rospy.get_caller_id() + " Boat State = 'Autonomous - Tacking'")
		
		pid_controller.setTarget(target_heading)
		while pid_controller.isOnTarget():
			pass
			
		state.minor = BoatState.MIN_PLANNING
		boat_state_pub.publish(state)		
		rospy.loginfo(rospy.get_caller_id() + " Boat State = 'Autonomous - Planning'")
	
	# Otherwise, we don't need to tack, so simply update the controller's setpoint
	else:		
		pid_controller.setGoal(target_heading)



def joy_callback(controller):
    global rudder_pos
    global rudder_pos_pub
    global state

    if state.minor is not BoatState.MIN_TACKING:
        # If the boat is not currently tacking, then setup a message to send to the /rudder topic
        rudder_pos_old = rudder_pos
        position_msg = Float32()

        # Set the rudder position to be a min of 30 and max of 150
        position_msg.data = (90 - (60 * controller.axes[0]))

        # Only publish if the change in rudder angle is greater than 5
        if abs(position_msg.data - rudder_pos_old) > 5:
            rudder_pos_pub.publish(position_msg)
            rospy.loginfo(rospy.get_caller_id() + " Read value: %f", controller.axes[0])
            rudder_pos = position_msg.data

    
def listener():
    # Setup subscribers
    rospy.init_node('joy_to_rudder', anonymous=True)
    rospy.Subscriber('joy', Joy, joy_callback)
    rospy.Subscriber('boat_state', BoatState, boat_state_callback)
    rospy.Subscriber('wind_heading', Float32, wind_callback)
    rospy.Subscriber('target_heading', Float32, heading_callback)
    rospy.spin()
    

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
