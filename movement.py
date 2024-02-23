import sys
import time
from pymavlink import mavutil

# Start a connection listening to a UDP port
the_connection = mavutil.mavlink_connection('udpin:localhost:14551')

# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("connection! from system (system %u component %u)" %
      (the_connection.target_system, the_connection.target_component))



mode='TAKEOFF'
#checking for mode availability
if mode not in the_connection.mode_mapping():
	print('Unknown mode: {}'.format(mode))
	print('Try: ',list(the_connection.mode_mapping().keys()))
	sys.exit(1)
	
#Get mode id
mode_id=the_connection.mode_mapping()[mode]
#arming
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                         mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

time.sleep(6)  

#takeoff
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                         mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0, 1, 13, 0, 0, 0, 0, 0)
#the_connection.mav.set_mode_send(
#	the_connection.target_system,
#	mavutil.mavlink.MAV_NODE_FLAG_CUSTOM_MODE_ENABLED,
#	mode_id)

print("mode changed")

#time.sleep(11)
#guided
#the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
#                                         mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0, 1, 15, 0, 0, 0, 0, 0)

time.sleep(7)

#waypoint
the_connection.mav.command_int_send(the_connection.target_system, the_connection.target_component,
					  mavutil.mavlink.MAV_FRAME_GLOBAL,
                                         mavutil.mavlink.MAV_CMD_DO_REPOSITION, 0, 0, -1, 1, 15, 1, 100, 100, 60)

#the_connection.mav.mission_item_int(the_connection.target_system, the_connection.target_component, 0,
#                                         mavutil.mavlink.MAV_FRAME_GLOBAL,
#                                         mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 2, 2, 0, 100, 100, 60)
print("waypoint set")
#the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, #the_connection.target_system,
#                         the_connection.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b010111111000), 40, 0, -10, 0, 0, 0, 0, 0, 0, 1.57, 0.5))

#the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, the_connection.target_system,
#                        the_connection.target_component, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, int(0b110111111000), int(-35.3629849 * 10 ** 7), int(149.1649185 * 10 ** 7), 10, 0, 0, 0, 0, 0, 0, 1.57, 0.5))


#while 1:
#    msg = the_connection.recv_match(
#        type='LOCAL_POSITION_NED', blocking=True)
#    print(msg)
