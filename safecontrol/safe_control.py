import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import time
import argparse

class SafeArmController(Node):
    def __init__(self):
        super().__init__('safe_arm_controller')
        self.publisher_ = self.create_publisher(JointTrajectory, '/arm_controller/joint_trajectory', 10)

    def move_arm(self, target_k1, target_k2):
        safe_k1 = max(-1.0, min(target_k1, 1.0))
        k2_min_dynamic = -1.0 
        k2_max = 1.0 

        if safe_k1 < 0:
            k2_min_dynamic = -1.0 + abs(safe_k1) * 1.6

        safe_k2 = max(k2_min_dynamic, min(target_k2, k2_max))

        print("\n------------------------------------------------")
        if safe_k1 != target_k1 or safe_k2 != target_k2:
            self.get_logger().warn(f'CẢNH BÁO: Góc [{target_k1}, {target_k2}] vi phạm giới hạn động học!')
            self.get_logger().warn(f'--> Giới hạn an toàn tại k1={safe_k1:.2f} là k2 thuộc [{k2_min_dynamic:.2f}, {k2_max:.2f}]')
            self.get_logger().warn(f'--> Đã hãm phanh tự động về: [{safe_k1:.2f}, {safe_k2:.2f}]')
        else:
            self.get_logger().info(f'Quỹ đạo an toàn. Đang chạy đến: [{safe_k1:.2f}, {safe_k2:.2f}]')
        print("------------------------------------------------\n")

        msg = JointTrajectory()
        msg.joint_names = ['khau1_joint', 'khau2_joint']
        
        point = JointTrajectoryPoint()
        point.positions = [float(safe_k1), float(safe_k2)]
        point.time_from_start = Duration(sec=3, nanosec=0) 
        
        msg.points.append(point)
        self.publisher_.publish(msg)

def main(args=None):
    parser = argparse.ArgumentParser(description='Điều khiển tay máy an toàn qua Terminal')
    parser.add_argument('goc_khau1', type=float, help='Góc mục tiêu cho khâu 1 (radian)')
    parser.add_argument('goc_khau2', type=float, help='Góc mục tiêu cho khâu 2 (radian)')
    parsed_args, ros_args = parser.parse_known_args()

    rclpy.init(args=ros_args)
    node = SafeArmController()
    time.sleep(0.5) 
    node.move_arm(parsed_args.goc_khau1, parsed_args.goc_khau2) 

    time.sleep(0.5)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()