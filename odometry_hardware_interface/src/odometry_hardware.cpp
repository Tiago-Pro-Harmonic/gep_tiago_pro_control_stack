#include "odometry_hardware_interface/odometry_hardware.hpp"

#include "hardware_interface/types/hardware_interface_type_values.hpp"

namespace odometry_hardware_interface {

hardware_interface::CallbackReturn OdometryHardware::on_init(
    const hardware_interface::HardwareComponentInterfaceParams& params) {
  if (hardware_interface::SensorInterface::on_init(params) !=
      hardware_interface::CallbackReturn::SUCCESS) {
    return hardware_interface::CallbackReturn::ERROR;
  }

  RCLCPP_INFO(rclcpp::get_logger("OdometryHardware"),
              "OdometryHardware on_init(), hardware '%s'", info_.name.c_str());

  std::string topic_name = "/mobile_base_controller/odom";
  auto it = info_.hardware_parameters.find("topic_name");
  if (it != info_.hardware_parameters.end()) {
    topic_name = it->second;
  }

  node_ = std::make_shared<rclcpp::Node>("odometry_hardware_node_" + info_.name);

  sub_ = node_->create_subscription<nav_msgs::msg::Odometry>(
      topic_name, rclcpp::SystemDefaultsQoS(),
      std::bind(&OdometryHardware::odom_callback, this, std::placeholders::_1));

  // Spin the node in a dedicated thread so read() stays non-blocking.
  executor_ = std::make_unique<rclcpp::executors::SingleThreadedExecutor>();
  executor_->add_node(node_);
  running_ = true;
  spinner_thread_ = std::thread([this]() {
    while (running_ && rclcpp::ok()) {
      executor_->spin_some();
    }
  });

  RCLCPP_INFO(rclcpp::get_logger("OdometryHardware"),
              "Subscribed to '%s'", topic_name.c_str());

  return hardware_interface::CallbackReturn::SUCCESS;
}

hardware_interface::CallbackReturn OdometryHardware::on_deactivate(
    const rclcpp_lifecycle::State& /*previous_state*/) {
  running_ = false;
  if (spinner_thread_.joinable()) {
    spinner_thread_.join();
  }
  return hardware_interface::CallbackReturn::SUCCESS;
}

std::vector<hardware_interface::StateInterface>
OdometryHardware::export_state_interfaces() {
  std::vector<hardware_interface::StateInterface> state_interfaces;
  const std::string& sensor_name = info_.sensors[0].name;

  state_interfaces.emplace_back(sensor_name, "position.x", &pos_x_);
  state_interfaces.emplace_back(sensor_name, "position.y", &pos_y_);
  state_interfaces.emplace_back(sensor_name, "position.z", &pos_z_);

  state_interfaces.emplace_back(sensor_name, "orientation.x", &ori_x_);
  state_interfaces.emplace_back(sensor_name, "orientation.y", &ori_y_);
  state_interfaces.emplace_back(sensor_name, "orientation.z", &ori_z_);
  state_interfaces.emplace_back(sensor_name, "orientation.w", &ori_w_);

  state_interfaces.emplace_back(sensor_name, "linear_velocity.x", &lin_vel_x_);
  state_interfaces.emplace_back(sensor_name, "linear_velocity.y", &lin_vel_y_);
  state_interfaces.emplace_back(sensor_name, "linear_velocity.z", &lin_vel_z_);

  state_interfaces.emplace_back(sensor_name, "angular_velocity.x", &ang_vel_x_);
  state_interfaces.emplace_back(sensor_name, "angular_velocity.y", &ang_vel_y_);
  state_interfaces.emplace_back(sensor_name, "angular_velocity.z", &ang_vel_z_);

  return state_interfaces;
}

hardware_interface::return_type OdometryHardware::read(
    const rclcpp::Time& /*time*/, const rclcpp::Duration& /*period*/) {
  // Data is updated in odom_callback() by the spinner thread.
  // Nothing to do here — the mutex ensures consistency.
  return hardware_interface::return_type::OK;
}

void OdometryHardware::odom_callback(
    const nav_msgs::msg::Odometry::SharedPtr msg) {
  std::lock_guard<std::mutex> lock(mutex_);

  pos_x_ = msg->pose.pose.position.x;
  pos_y_ = msg->pose.pose.position.y;
  pos_z_ = msg->pose.pose.position.z;

  ori_x_ = msg->pose.pose.orientation.x;
  ori_y_ = msg->pose.pose.orientation.y;
  ori_z_ = msg->pose.pose.orientation.z;
  ori_w_ = msg->pose.pose.orientation.w;

  lin_vel_x_ = msg->twist.twist.linear.x;
  lin_vel_y_ = msg->twist.twist.linear.y;
  lin_vel_z_ = msg->twist.twist.linear.z;

  ang_vel_x_ = msg->twist.twist.angular.x;
  ang_vel_y_ = msg->twist.twist.angular.y;
  ang_vel_z_ = msg->twist.twist.angular.z;
}

}  // namespace odometry_hardware_interface

#include "pluginlib/class_list_macros.hpp"
PLUGINLIB_EXPORT_CLASS(odometry_hardware_interface::OdometryHardware,
                       hardware_interface::SensorInterface)
