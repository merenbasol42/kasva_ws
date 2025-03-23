#!/usr/bin/env python3
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
import cv2
import numpy as np

from threading import Thread

from .config.compressor import *

class CompressorNode(Node):
    def __init__(self):
        super().__init__(NODE_NAME)
        self.publisher_ = self.create_publisher(CompressedImage, TOP_NAME_CAMERA_COMPRESSED, 10)
        
        self.last_extract = time.time()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.get_logger().error("Dahili kamera açılmıyor!")
            exit()

        self.buffer = None
        self.flag: bool = False
        self.msg = CompressedImage()
        self.msg.header.frame_id = FRAME_ID
        self.msg.format = "jpeg"  # veya "jpeg; compressed" gibi format belirtebilirsin

        Thread(target=self.extract_loop, daemon=True).start()
        Thread(target=self.publish_loop, daemon=True).start()
    
    def extract_loop(self):    
        interval: float = 0.0
        while True:
            interval = time.time() - self.last_extract
            if interval > HZ:
                ret, frame = self.cap.read()
                if not ret:
                    self.get_logger().warning("Kameradan görüntü alınamadı!")
                    continue

                # Görüntüyü JPEG formatında sıkıştır
                ret2, buffer = cv2.imencode('.jpg', frame)
                if not ret2:
                    self.get_logger().error("Görüntü sıkıştırılamadı!")
                    continue
                self.buffer = buffer
                self.flag = True

            else:
                time.sleep(HZ - interval)
                
    def publish_loop(self):
        while True:
            if self.flag:
                # CompressedImage mesajı oluşturma
                self.msg.header.stamp = self.get_clock().now().to_msg()
                self.msg.data = np.array(self.buffer).tobytes()
                self.publisher_.publish(self.msg)
                self.flag = False

            else:
                time.sleep(HZ)        


    def destroy_node(self):
        self.cap.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = CompressorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
