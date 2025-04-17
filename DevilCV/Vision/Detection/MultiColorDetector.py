from .Detector import MultiDetector
from .ColorDetector import ColorDetector
from DevilCV.utils.custom_types.Color import HSVColorRange
import cv2
from typing import List, Sequence

class MultiColorDetector(MultiDetector, ColorDetector):
    def __init__(self, ranges: List[HSVColorRange], det_names: List[str], area_threshold: int = 500, name: str = "MultiColorDetector"):
        self.area_threshold = area_threshold
        self.detectors = [ColorDetector(color_range, area_threshold, det_names[i]) for i, color_range in enumerate(ranges)]
        self.name = name

    def multidetect(self, hsv_frame):
        detections = {}
        for detector in self.detectors:
            detections[detector.name] = detector.detect(hsv_frame)
        return detections

    def multimask(self, hsv_frame):
        masks: dict[str, cv2.typing.MatLike] = {}
        contours: dict[str, Sequence[cv2.typing.MatLike]] = {}

        for detector in self.detectors:
            mask = cv2.inRange(hsv_frame, detector.color_range.get_lower(), detector.color_range.get_upper())
            contours[detector.name], _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            masks[detector.name] = mask
            filtered_contours = [cnt for cnt in contours[detector.name] if cv2.contourArea(cnt) > self.area_threshold]
            contours[detector.name] = filtered_contours
        return contours, masks
    
    
    def multicenters(self, contours):
        centers = {}
        for name, contour_list in contours.items():
            centers[name] = []
            local_centers = super().centers(contour_list)
            centers[name].extend(local_centers)
        return centers
    
    
