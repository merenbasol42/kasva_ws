import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan

#
# Logic
#

class AsyncObsAvo(Node):
    def __init__(self):
        super().__init__("kasva_obs_avo")

    #
    # ROS Methods
    #

    def scan_cb(self, msg: LaserScan) -> None:
        pass

    def pub_cmd_vel(self, linear: float, angular: float) -> None:
        pass
    
    #
    # External Access
    #

    def mainloop(self):
        while rclpy.ok():
            if self.detect():
                # Eğer engel tespit edildiyse
                if not self.warn():
                    # Eğer engel ortadan kalkmamışsa
                    self.avoid()
            else:
                pass

    #
    # 
    #

    def detect(self) -> bool:
        pass

    def warn() -> bool:
        pass

    def avoid(self):
        pass

    #
    # Tools
    #
    

#
# Entry Point
#

def main():
    rclpy.init()
    node = AsyncObsAvo()
    try: rclpy.spin(node)
    except: pass
    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()