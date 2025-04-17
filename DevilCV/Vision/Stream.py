import cv2
from DevilCV.Vision.Detection.MultiColorDetector import MultiDetector
from typing import Optional
from DevilCV.utils.custom_types.Detection import CenterCallback


class Stream:
    def __init__(self, source: int, exposure: int, multi_detectors: list[MultiDetector], show: bool = True):
        self.source = source
        self.multi_detectors = multi_detectors
        self.capture = cv2.VideoCapture(source)
        self.capture.set(cv2.CAP_PROP_EXPOSURE, exposure)
        self.show = show

        if not self.capture.isOpened():
            raise ValueError(f"Cannot open video source {source}")
        
    def start(self, callback: Optional[CenterCallback] = None):
        while True:
            ret, frame = self.capture.read()
            if not ret:
                break

            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            all_detections = {}
            for multi_detector in self.multi_detectors:
                detections_dict = multi_detector.multidetect(hsv_frame)
                all_detections[multi_detector.name] = detections_dict

                for name, detections in detections_dict.items():
                    for detection in detections:
                        x, y, w, h = detection.bounding_box
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(frame, f"{name}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        cv2.circle(frame, detection.center, 5, (0, 0, 255), -1)


                        

            if callback:
                callback(all_detections)

            if self.show:
                cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.capture.release()
        cv2.destroyAllWindows()