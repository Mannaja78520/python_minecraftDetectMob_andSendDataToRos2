import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    # microros_launch_path = PathJoinSubstitution(
    #     [FindPackageShare("labtop_node"), "launch", "microros.launch.py"]
    # )
    
    robot_run_node = Node(
        package="laptop_node",
        # output="screen",
        executable="main"
    )
    
    # launch_microros = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(microros_launch_path),
    # )
    # ld.add_action(launch_microros)
    ld.add_action(robot_run_node)
    
    # os.system("gnome-terminal -e 'bash -c \"ros2 launch robot_core microros.launch.py\"'")
    # os.system("gnome-terminal -e 'bash -c \"ros2 launch robot_core microros.launch.py\"'")
    
    return ld