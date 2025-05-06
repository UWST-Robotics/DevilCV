import cv2
from DevilCV.Vision.Detection.MultiColorDetector import MultiDetector
from typing import Optional
from DevilCV.utils.custom_types.Detection import CenterCallback
from mjpeg_streamer import MjpegServer, Stream as MjpegStream
from dotenv import load_dotenv
import os

load_dotenv()

CAPTURE_API = cv2.CAP_ANY if os.getenv("DEVICE", "pi") == "pi" else cv2.CAP_DSHOW 
stream = MjpegStream("DevilCV", size=(640, 480), quality=50, fps=30) 

server = MjpegServer("localhost", 8080)
server.add_stream(stream) 
server.start()
class Stream:
    def __init__(self, source: int, exposure: float, multi_detectors: list[MultiDetector], invert: bool = False, show: bool = True):
        self.source = source
        self.multi_detectors = multi_detectors
        self.capture = cv2.VideoCapture(source, CAPTURE_API)
        self.capture.set(cv2.CAP_PROP_EXPOSURE, exposure)
        self.invert = invert

        
    
        self.show = show
        self.resolution = (int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        if not self.capture.isOpened():
            raise ValueError(f"Cannot open video source {source}")
        
    def start(self, callback: Optional[CenterCallback] = None, record: bool = False):
        video_writer = None
        if record:
            # Get the frame width and height
            frame_width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fourcc = cv2.VideoWriter_fourcc(*'XVID',) # type: ignore[no-untyped-call]
            video_writer = cv2.VideoWriter("out.avi", fourcc, 20.0, (frame_width, frame_height))

        while True:
            ret, frame = self.capture.read()
            if not ret:
                break

            if self.invert:
                frame = cv2.rotate(frame, cv2.ROTATE_180)
            blurred_frame = cv2.GaussianBlur(frame, (21, 21), 0)
            # frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2RGB)
            hsv_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
            all_detections = {}
            for multi_detector in self.multi_detectors:
                detections_dict = multi_detector.multidetect(hsv_frame)
                all_detections[multi_detector.name] = detections_dict

                for name, detections in detections_dict.items():
                    if len(detections) == 0:
                        continue
                    x, y, w, h = detections[0].bounding_box
                    if self.show:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(frame, f"{name}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        cv2.circle(frame, detections[0].center, 5, (0, 0, 255), -1)


                        

            if callback:
                callback(all_detections)

            if record and video_writer:
                video_writer.write(frame)

            if self.show:
                stream.set_frame(frame) 
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        if video_writer:
            video_writer.release()
        self.capture.release()
        cv2.destroyAllWindows()