import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    package_name = 'Assem1'
    pkg_share = get_package_share_directory(package_name)
    urdf_file = os.path.join(pkg_share, 'urdf', 'Assem1.urdf')
    world_file = os.path.join(pkg_share, 'worlds', 'map.world') 
    rviz_config_file = os.path.join(pkg_share, 'rviz', 'view_robot.rviz')

    # Đọc nội dung file URDF
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    # Thiết lập đường dẫn để Gazebo tìm thấy file Mesh (STL/DAE)
    pkg_parent = os.path.dirname(pkg_share)
    set_gazebo_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=pkg_parent
    )

    # Node: robot_state_publisher
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': True 
        }]
    )

    # Khởi chạy Gazebo
    gazebo_pkg_dir = get_package_share_directory('gazebo_ros')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_pkg_dir, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': world_file}.items() 
    )

    # Node: spawn robot
    spawn_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'Assem1',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.1' 
        ],
        output='screen'
    )

    # Node: Bật RViz2
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': True}] 
    )

    return LaunchDescription([
        set_gazebo_model_path,
        rsp_node,
        gazebo,
        spawn_node,
        rviz_node  
    ])