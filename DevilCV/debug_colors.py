import cv2
import imutils
from DevilCV.utils.custom_types.Color import HSVColor, HSVColorRange
from DevilCV.Vision.Detection.MultiColorDetector import MultiColorDetector

detectors = {
    "Red": [HSVColorRange(HSVColor(160, 100, 100), HSVColor(179, 255, 255)), HSVColorRange(HSVColor(0, 100, 100), HSVColor(20, 255, 255))],
    "Blue": [HSVColorRange(HSVColor(100, 100, 92), HSVColor(124, 255, 255))],
}

multi_detector = MultiColorDetector(detectors, 1000)

vs = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    
class HSVTrackbar:
    def __init__(self, window_name: str, lower: HSVColor, upper: HSVColor):
        self.lower = lower
        self.upper = upper
        cv2.namedWindow(window_name)
        cv2.createTrackbar("Lower H", window_name, lower.h, 179, self.update_lower_h)
        cv2.createTrackbar("Lower S", window_name, lower.s, 255, self.update_lower_s)
        cv2.createTrackbar("Lower V", window_name, lower.v, 255, self.update_lower_v)
        cv2.createTrackbar("Upper H", window_name, upper.h, 179, self.update_upper_h)
        cv2.createTrackbar("Upper S", window_name, upper.s, 255, self.update_upper_s)
        cv2.createTrackbar("Upper V", window_name, upper.v, 255, self.update_upper_v)
    def update_lower_h(self, value: int):
        self.lower.h = value
    def update_lower_s(self, value: int):
        self.lower.s = value
    def update_lower_v(self, value: int):
        self.lower.v = value
    def update_upper_h(self, value: int):
        self.upper.h = value
    def update_upper_s(self, value: int):
        self.upper.s = value
    def update_upper_v(self, value: int):
        self.upper.v = value
    
    


red_1_trackbar = HSVTrackbar("Red", detectors["Red"][0].lower, detectors["Red"][0].upper)
red_2_trackbar = HSVTrackbar("Red", detectors["Red"][1].lower, detectors["Red"][1].upper)

blues = HSVColorRange(HSVColor(0, 0, 0), HSVColor(179, 255, 255))
blue_trackbar = HSVTrackbar("Blue", blues.lower, blues.upper)


while True:
    ret, frame = vs.read()
    frame = imutils.resize(frame, width=400)
    blurred = cv2.GaussianBlur(frame, (41, 41), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    contours, masks = multi_detector.multimask(hsv)

    # draw contours and masks
    for name, mask in masks.items():
        cv2.imshow(f"{name} Mask", mask)
        for contour in contours[name]:
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(frame, (cX, cY), 7, (255, 0, 0), -1)
                cv2.putText(frame, f"{name}", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                

    # draw the original frame with contours
    cv2.imshow("Frame", frame)
    cv2.imshow("HSV", hsv)
    cv2.imshow("Blurred", blurred)
    cv2.imshow("Red Mask", masks["Red"])
    cv2.imshow("Blue Mask", masks["Blue"])


    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break


cv2.destroyAllWindows()

