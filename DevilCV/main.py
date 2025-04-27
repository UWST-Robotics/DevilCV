from DevilCV.Vision.Stream import Stream
from DevilCV.Vision.Detection.MultiColorDetector import MultiColorDetector
from DevilCV.utils.custom_types.Color import HSVColorRange, HSVColor
from DevilCV.utils.custom_types.Detection import Detections
from DevilCV.Bridge.Bridge import Bridge
from DevilCV.utils.coordinates import top_left_to_center_relative
from dotenv import load_dotenv
import os

load_dotenv()

VEXBRIDGE_HOST = os.getenv("VEXBRIDGE_HOST", "localhost")
VEXBRIDGE_PORT = int(os.getenv("VEXBRIDGE_PORT", 8000))
CAMERA_EXPOSURE = int(os.getenv("CAMERA_EXPOSURE", -6))

def main():

    detectors = {
        "Red": [HSVColorRange(HSVColor(160, 100, 100), HSVColor(179, 255, 255)), HSVColorRange(HSVColor(0, 100, 100), HSVColor(20, 255, 255))],
        "Blue": [HSVColorRange(HSVColor(100, 100, 92), HSVColor(124, 255, 255))],
    }

    multi_detector = MultiColorDetector(detectors, 1000)

    bridge = Bridge(host=VEXBRIDGE_HOST, port=VEXBRIDGE_PORT)
    stream = Stream(source=0, exposure=CAMERA_EXPOSURE, multi_detectors=[multi_detector], show=True)

    def callback(center_detections: Detections):
        red_detections = center_detections['MultiColorDetector']['Red'] if 'Red' in center_detections['MultiColorDetector'] else []
        blue_detections = center_detections['MultiColorDetector']['Blue'] if 'Blue' in center_detections['MultiColorDetector'] else []
        
        if len(red_detections) == 0: 
            red_center_x = None
            red_edge_x = None
        else:
            red_center_x = red_detections[0].center[0]
            red_edge_x = red_detections[0].bounding_box[0]

        if len(blue_detections) == 0:
            blue_center_x = None
            blue_edge_x = None
        else:
            blue_center_x = blue_detections[0].center[0]
            blue_edge_x = blue_detections[0].bounding_box[0]

        red_center_x, _ = top_left_to_center_relative(red_center_x, 0, stream.resolution) if red_center_x is not None else (None, None)
        red_edge_x, _ = top_left_to_center_relative(red_edge_x, 0, stream.resolution) if red_edge_x is not None else (None, None)
        blue_center_x, _ = top_left_to_center_relative(blue_center_x, 0, stream.resolution) if blue_center_x is not None else (None, None)
        blue_edge_x, _ = top_left_to_center_relative(blue_edge_x, 0, stream.resolution) if blue_edge_x is not None else (None, None)

        values = {}

        if red_center_x is not None:
            values['vision/color/red/center_x'] = red_center_x
        if red_edge_x is not None:
            values['vision/color/red/edge_x'] = red_edge_x
        if blue_center_x is not None:
            values['vision/color/blue/center_x'] = blue_center_x
        if blue_edge_x is not None:
            values['vision/color/blue/edge_x'] = blue_edge_x
        values['vision/hasTarget'] = len(values) > 0

        
        bridge.set_values(values)


    stream.start(callback, record=True)

if __name__ == "__main__":
    main()