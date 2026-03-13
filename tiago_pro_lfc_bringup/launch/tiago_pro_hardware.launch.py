from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

# TODO: real robot bringup
# This launch file handles connection to the physical TIAGo Pro and spawns the
# LFC controller chain. Before launching, ensure:
#   - robot is powered on and initialized
#   - CycloneDDS is configured (RMW_IMPLEMENTATION, CYCLONEDDS_URI, ROS_DOMAIN_ID)
#   - linear_feedback_controller is deployed on the robot via pal deploy tooling


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument("pkg", default_value="tiago_pro_lfc_bringup"),
            DeclareLaunchArgument(
                "lfc_yaml",
                default_value="config/fixed/linear_feedback_controller_params.yaml",
            ),
            DeclareLaunchArgument(
                "jse_yaml",
                default_value="config/fixed/joint_state_estimator_params.yaml",
            ),
            DeclareLaunchArgument(
                "pc_yaml", default_value="config/fixed/dummy_controllers.yaml"
            ),
            # LFC controller chain
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution(
                        [
                            FindPackageShare("tiago_pro_lfc_bringup"),
                            "launch",
                            "switch_to_lfc_controllers.launch.py",
                        ]
                    )
                ),
                launch_arguments={
                    "pkg": LaunchConfiguration("pkg"),
                    "lfc_yaml": LaunchConfiguration("lfc_yaml"),
                    "jse_yaml": LaunchConfiguration("jse_yaml"),
                    "pc_yaml": LaunchConfiguration("pc_yaml"),
                }.items(),
            ),
        ]
    )
