from typing import List, Optional, Sequence, Tuple
from DevilCV.utils.custom_types.Color import HSVColorRange
from DevilCV.utils.custom_types.Detection import Detection
import cv2
from DevilCV.Vision.Detection.Detector import Detector


class ColorDetector(Detector):
    def __init__(self, color_range: HSVColorRange, area_threshold: int = 500, name: Optional[str] = None):
        self.color_range = color_range
        self.area_threshold = area_threshold
        self.name = name if name else f"ColorDetector_{color_range.get_lower()}_{color_range.get_upper()}"

    def detect(self, hsv_frame):
        contours, mask = self.mask(hsv_frame)
        centers = self.centers(contours)
        
        detections = []

        for i, contour in enumerate(contours):
            # bounding box
            detections.append(
                Detection(
                    bounding_box=cv2.boundingRect(contour),
                    center=centers[i]
                )
            )
            
        return detections


    def mask(self, hsv_frame):
        mask = cv2.inRange(hsv_frame, self.color_range.get_lower(), self.color_range.get_upper())
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        mask = cv2.erode(mask, kernel, iterations=2)
        mask = cv2.dilate(mask, kernel, iterations=2)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = [cnt for cnt in contours if cv2.contourArea(cnt) > self.area_threshold]
        return contours, mask
    
    def centroid(self, contour: cv2.typing.MatLike):
        M = cv2.moments(contour)
        if M["m00"] == 0:
            return None
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return (cX, cY)
    
    def centers(self, contours):
        centers: List[Tuple[int, int]] = []
        for contour in contours:
            center = self.centroid(contour)
            if center:
                centers.append(center)
        return centers
    
        