from DevilCV.Vision.Stream import Stream
from DevilCV.Vision.Detection.MultiColorDetector import MultiColorDetector
from DevilCV.utils.custom_types.Color import HSVColorRange, HSVColor
from DevilCV.utils.custom_types.Detection import Detections
from DevilCV.Bridge.Bridge import Bridge
from DevilCV.utils.coordinates import top_left_to_center_relative

def main():

    detectors = {
        "Red": [HSVColorRange(HSVColor(160, 100, 100), HSVColor(179, 255, 255)), HSVColorRange(HSVColor(0, 100, 100), HSVColor(20, 255, 255))],
        "Blue": [HSVColorRange(HSVColor(100, 100, 92), HSVColor(124, 255, 255))],
    }

    multi_detector = MultiColorDetector(detectors, 1000)

    bridge = Bridge("localhost", 8000)
    stream = Stream(source=0, exposure=-6, multi_detectors=[multi_detector], show=True)

    def callback(center_detections: Detections):
        # red_center_x = center_detections['MultiColorDetector']['Red'][0].center[0] if 'Red' in center_detections['MultiColorDetector'] else None
        # red_edge_x = center_detections['MultiColorDetector']['Red'][0].bounding_box[0] if 'Red' in center_detections['MultiColorDetector'] else None
        # blue_center_x = center_detections['MultiColorDetector']['Blue'][0].center[0] if 'Blue' in center_detections['MultiColorDetector'] else None
        # blue_edge_x = center_detections['MultiColorDetector']['Blue'][0].bounding_box[0] if 'Blue' in center_detections['MultiColorDetector'] else None
        
        # red_center_x, _ = top_left_to_center_relative(red_center_x, 0, stream.resolution) if red_center_x is not None else (None, None)
        # red_edge_x, _ = top_left_to_center_relative(red_edge_x, 0, stream.resolution) if red_edge_x is not None else (None, None)
        # blue_center_x, _ = top_left_to_center_relative(blue_center_x, 0, stream.resolution) if blue_center_x is not None else (None, None)
        # blue_edge_x, _ = top_left_to_center_relative(blue_edge_x, 0, stream.resolution) if blue_edge_x is not None else (None, None)

        # # send only non-null values to the bridge
        # values = {}
        # if red_center_x is not None:
        #     values['vision/color/red/center_x'] = red_center_x
        # if red_edge_x is not None:
        #     values['vision/color/red/edge_x'] = red_edge_x
        # if blue_center_x is not None:
        #     values['vision/color/blue/center_x'] = blue_center_x
        # if blue_edge_x is not None:
        #     values['vision/color/blue/edge_x'] = blue_edge_x
        print(center_detections)

        # bridge.set_values(values)

    stream.start(callback, record=True)

if __name__ == "__main__":
    main()