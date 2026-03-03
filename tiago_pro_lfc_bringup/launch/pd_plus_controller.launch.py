from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    RegisterEventHandler,
    LogInfo,
)
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.event_handlers import OnProcessExit


def generate_launch_description():

    # pd_plus_controller node
    pd_plus_controller_params = PathJoinSubstitution(
        [
            FindPackageShare("tiago_pro_lfc_bringup"),
            "config",
            "pd_plus_controller_params.yaml",
        ]
    )
    pd_plus_controller_node = Node(
        package="linear_feedback_controller",
        executable="pd_plus_controller",
        parameters=[pd_plus_controller_params],
        output="screen",
    )



    return LaunchDescription(
        [
            pd_plus_controller_node
        ]
    )