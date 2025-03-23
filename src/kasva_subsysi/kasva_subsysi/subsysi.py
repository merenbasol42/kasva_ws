
import rclpy
from rclpy.node import Node
from .config.subsysi import *

from geometry_msgs.msg import Quaternion
from std_msgs.msg import String

#
# Logic
#

class SubsysiNode(Node):
    def __init__(self):
        super().__init__(NODE_NAME)
        
        self.create_subscription(Quaternion, TOP_NAME_MC_ENC_STATS, self.mc_enc_stats_cb, 5)
        self.create_subscription(String, TOP_NAME_MC_OUT, self.mc_out_cb, 5)

    def mc_enc_stats_cb(self, msg: Quaternion):
        pass

    def mc_out_cb(self, msg: String):
        self.get_logger().info(msg.data)

#
# Entry Point
#

def main():
    rclpy.init()
    node = SubsysiNode()
    try: rclpy.spin(node)
    except: pass
    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()