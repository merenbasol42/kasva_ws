import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node

def generate_launch_description():
    # TurtleBot3 world dosyasının hazır yolu (örneğin, Humble için)
    gazebo_world = '/opt/ros/humble/share/turtlebot3_gazebo/worlds/turtlebot3_world.sdf'
    
    return LaunchDescription([
        # 1. Gazebo Fortress'u world dosyası ile başlat
        ExecuteProcess(
            cmd=['ign', 'gazebo', '-r', gazebo_world],
            output='screen'
        ),
        # 2. 5 saniye gecikme sonrası ros_ign_bridge'i başlat (tüm topic'ler için)
        TimerAction(
            period=5.0,
            actions=[
                Node(
                    package='ros_ign_bridge',
                    executable='parameter_bridge',
                    arguments=['--bridge-all'],
                    output='screen'
                )
            ]
        ),
        # 3. 7 saniye gecikme sonrası TurtleBot3'ü spawn et
        # Burada, robotu spawn eden hazır bir node veya servis kullanabilirsin.
        TimerAction(
            period=7.0,
            actions=[
                Node(
                    package='turtlebot3_spawn_package',  # Bu kısımda uygun paketi kullanmalısın
                    executable='spawn_turtlebot3',
                    name='spawn_turtlebot3',
                    output='screen'
                )
            ]
        )
    ])
