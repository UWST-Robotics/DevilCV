from .Detector import MultiDetector
from .ColorDetector import ColorDetector
from DevilCV.utils.custom_types.Color import HSVColorRange, DetectorDict
import cv2
from typing import List, Sequence

class MultiColorDetector(MultiDetector, ColorDetector):
    def __init__(self, detectors: DetectorDict, area_threshold: int = 500, name: str = "MultiColorDetector"):
        self.area_threshold = area_threshold
        # if the same name is provided for multiple detectors ranges, the detector with that name will have multiple ranges
        self.detectors = [ColorDetector(color_range, area_threshold, name) for name, color_range in detectors.items()]

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
            contours[detector.name], masks[detector.name] = detector.mask(hsv_frame)
        return contours, masks
    
    
    def multicenters(self, contours):
        centers = {}
        for name, contour_list in contours.items():
            centers[name] = []
            local_centers = super().centers(contour_list)
            centers[name].extend(local_centers)
        return centers
    
    
