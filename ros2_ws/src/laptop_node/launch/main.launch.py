import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    robot_run_node = Node(
        package="laptop_node",
        # output="screen",
        executable="main"
    )
    
    ld.add_action(robot_run_node)
    
    return ld