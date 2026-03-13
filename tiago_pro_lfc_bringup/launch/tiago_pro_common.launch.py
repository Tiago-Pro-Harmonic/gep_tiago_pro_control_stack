from launch import LaunchContext, LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_entity import LaunchDescriptionEntity
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def launch_setup(
    context: LaunchContext, *args, **kwargs
) -> list[LaunchDescriptionEntity]:
    use_gazebo_bool = (
        context.perform_substitution(LaunchConfiguration("use_gazebo")).lower() == "true"
    )

    shared_lfc_args = {
        "pkg": LaunchConfiguration("pkg"),
        "lfc_yaml": LaunchConfiguration("lfc_yaml"),
        "jse_yaml": LaunchConfiguration("jse_yaml"),
        "pc_yaml": LaunchConfiguration("pc_yaml"),
    }

    if use_gazebo_bool:
        robot_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution(
                    [
                        FindPackageShare("tiago_pro_lfc_bringup"),
                        "launch",
                        "tiago_pro_simulation.launch.py",
                    ]
                )
            ),
            launch_arguments={
                **shared_lfc_args,
                "world_name": LaunchConfiguration("world_name"),
                "arm_type_right": LaunchConfiguration("arm_type_right"),
                "arm_type_left": LaunchConfiguration("arm_type_left"),
                "end_effector_right": LaunchConfiguration("end_effector_right"),
                "end_effector_left": LaunchConfiguration("end_effector_left"),
                "tuck_arm": LaunchConfiguration("tuck_arm"),
                "has_wrist_camera": LaunchConfiguration("has_wrist_camera"),
            }.items(),
        )
    else:
        robot_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution(
                    [
                        FindPackageShare("tiago_pro_lfc_bringup"),
                        "launch",
                        "tiago_pro_hardware.launch.py",
                    ]
                )
            ),
            launch_arguments=shared_lfc_args.items(),
        )

    return [robot_launch]


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_gazebo",
                default_value="true",
                choices=["true", "false"],
                description="Use Gazebo simulation. If false, connects to real robot.",
            ),
            # Simulation-only args (ignored when use_gazebo=false)
            DeclareLaunchArgument("world_name", default_value="empty"),
            DeclareLaunchArgument(
                "arm_type_left",
                default_value="tiago-pro",
                choices=["tiago-pro", "no-arm"],
            ),
            DeclareLaunchArgument(
                "arm_type_right",
                default_value="tiago-pro",
                choices=["tiago-pro", "no-arm"],
            ),
            DeclareLaunchArgument(
                "end_effector_right",
                default_value="pal-pro-gripper",
                choices=["pal-pro-gripper", "custom", "no-end-effector"],
            ),
            DeclareLaunchArgument(
                "end_effector_left",
                default_value="pal-pro-gripper",
                choices=["pal-pro-gripper", "custom", "no-end-effector"],
            ),
            DeclareLaunchArgument(
                "tuck_arm", default_value="False", choices=["True", "False"]
            ),
            DeclareLaunchArgument(
                "has_wrist_camera", default_value="True", choices=["True", "False"]
            ),
            # LFC config args (passed to switch_to_lfc_controllers)
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
            OpaqueFunction(function=launch_setup),
        ]
    )
