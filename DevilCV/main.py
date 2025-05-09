import threading
from DevilCV.Vision.Stream import Stream
from DevilCV.Vision.Detection.MultiColorDetector import MultiColorDetector
from DevilCV.utils.custom_types.Color import HSVColorRange, HSVColor
from DevilCV.utils.custom_types.Detection import Detections
from DevilCV.Bridge.Bridge import Bridge
from DevilCV.utils.coordinates import top_left_to_center_relative
from DevilCV.Bridge.Server import Server
from mjpeg_streamer import MjpegServer, Stream as MjpegStream
from dotenv import load_dotenv
import os

load_dotenv()

VEXBRIDGE_HOST = os.getenv("VEXBRIDGE_HOST", "localhost")
VEXBRIDGE_PORT = int(os.getenv("VEXBRIDGE_PORT", 8080))
SERVER_HOST = os.getenv("SERVER_HOST", "localhost")
SERVER_PORT = int(os.getenv("SERVER_PORT", 5000))
CAMERA_EXPOSURE = float(os.getenv("CAMERA_EXPOSURE", -6))
INVERT_CAMERA = os.getenv("CAMERA_INVERT", "False").lower() == "true"
CAMERA_SOURCE = int(os.getenv("CAMERA_SOURCE", 1))

DEFAULT_DETECTORS = {
    "Red": [HSVColorRange(HSVColor(160, 100, 100), HSVColor(179, 255, 255)), HSVColorRange(HSVColor(0, 100, 100), HSVColor(20, 255, 255))],
    "Blue": [HSVColorRange(HSVColor(100, 100, 92), HSVColor(124, 255, 255))],
}
def main():


    multi_detector = MultiColorDetector(DEFAULT_DETECTORS, 1000)

    server = Server(host=SERVER_HOST, port=SERVER_PORT)
    bridge = Bridge(host=VEXBRIDGE_HOST, port=VEXBRIDGE_PORT)
    mpjeg_stream = MjpegStream("DevilCV", size=(640, 480), quality=50, fps=30)
    mpjeg_server = MjpegServer("localhost", 5001)
    mpjeg_server.add_stream(mpjeg_stream)
    
    stream = Stream(source=CAMERA_SOURCE, exposure=CAMERA_EXPOSURE, invert=INVERT_CAMERA, stream=mpjeg_stream)

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

        print(values)
        # bridge.set_values(values)


    mpjeg_server.start()
    # Create threads for the Flask server and the stream
    flask_thread = threading.Thread(target=run_flask_server, args=(server, multi_detector))
    stream_thread = threading.Thread(target=run_stream, args=(stream, multi_detector, callback))

    # Start both threads
    flask_thread.start()
    stream_thread.start()

    # Wait for both threads to finish
    flask_thread.join()
    stream_thread.join()


def run_flask_server(server, multi_detector):
    """Run the Flask server."""
    server.start(multi_detector)

def run_stream(stream, multi_detector, callback):
    """Run the video stream."""
    stream.start([multi_detector], callback, record=True)


if __name__ == "__main__":
    main()