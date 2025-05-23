import sys
import expressive_motion_generation.trajectory_planner
from expressive_motion_generation.expressive_planner import ExpressivePlanner
from expressive_motion_generation.utils import make_point_at_task, make_point_at_task_from
from expressive_motion_generation.animation_execution import Animation
from expressive_motion_generation.effects import *
import rospy
import geometry_msgs
import moveit_commander
import moveit_msgs.msg
import numpy as np
import matplotlib.pyplot as plt
# initialize moveit 
moveit_commander.roscpp_initialize(sys.argv)

# instantiate Robot Commander
robot = moveit_commander.RobotCommander()
active_joints = robot.get_active_joint_names()

# create expressive planner
planner = ExpressivePlanner(robot=robot, publish_topic='joint_command', fake_display=False)
robot.get_group('panda_arm').set_end_effector_link('panda_hand')

group: moveit_commander.move_group.MoveGroupCommander = robot.get_group('panda_arm')

upper_limits = [joint.max_bound() for joint in (robot.get_joint(joint_name) for joint_name in robot.get_active_joint_names('panda_arm'))]
lower_limits = [joint.min_bound() for joint in (robot.get_joint(joint_name) for joint_name in robot.get_active_joint_names('panda_arm'))]

# try out a pose
pose_goal = geometry_msgs.msg.Pose()
pose_goal.orientation.w = -0.2
pose_goal.orientation.x = -0.6
pose_goal.orientation.y = -0.2
pose_goal.orientation.z = -0.6
pose_goal.position.x = 0.4
pose_goal.position.y = 0.01
pose_goal.position.z = 0.6

# planner.new_plan()
# planner.plan_animation("/home/mwiebe/noetic_ws/IsaacSim-ros_workspaces/noetic_ws/panda_animations/animation_happy2.yaml")
# # planner.at(0).add_effects(GazeEffect([0.6, 0, 0.6], 'panda_hand', 'panda_arm', start_index=3, stop_index=17))
# planner.at(0).add_effects(GazeEffect(point=[0, 3, 0], 
#                                      link='panda_hand', 
#                                      move_group='panda_arm', 
#                                      start_index=3, 
#                                      stop_index=17))
# planner.plan_target(pose_goal, 'panda_arm', 1.0, 1.0, 'pose')
# planner.at(1).add_effects(JitterEffect(0.02))
# planner.bake()
# planner.add_task(make_point_at_task_from(robot, 'panda_arm', [1.6, 0, 0.6], 'panda_hand', planner.get_last_joint_state(), 2))
# planner.execute()

planner.new_plan()
print('plan anim')
planner.plan_animation("/home/mwiebe/noetic_ws/IsaacSim-ros_workspaces/noetic_ws/panda_animations/animation_happy2.yaml")
planner.get_task_at(0).add_effects(ExtentEffect(0.1, ['g','n','g','p','m','p','i','i'], upper_limits, lower_limits))
planner.get_task_at(0).add_effects(GazeEffect([0.6, 0, 0.6], 'panda_hand', 'panda_arm', start_index=3, stop_index=17))
planner.get_task_at(0).add_effects(JitterEffect())
planner.bake()
planner.execute()
