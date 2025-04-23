import cv2
import imutils
import numpy as np



vs = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# low exposure

vs.set(cv2.CAP_PROP_EXPOSURE, -7)
lower_red = np.array([0, 178, 100])
upper_red = np.array([255, 255, 100])
lower_blue = np.array([100, 100, 100])
upper_blue = np.array([140, 255, 100])


class HSVColor:
    def __init__(self, h: int, s: int, v: int):
        self.hsv = np.array([h, s, v], dtype=np.uint8)

    @property
    def h(self):
        return self.hsv[0]
    @h.setter
    def h(self, value: int):
        self.hsv[0] = value
    @property
    def s(self):
        return self.hsv[1]
    @s.setter
    def s(self, value: int):
        self.hsv[1] = value
    @property
    def v(self):
        return self.hsv[2]
    @v.setter
    def v(self, value: int):
        self.hsv[2] = value

class HSVColorRange:
    def __init__(self, lower: HSVColor, upper: HSVColor):
        self.lower = lower
        self.upper = upper
    def get_lower(self):
        return self.lower.hsv
    def get_upper(self):
        return self.upper.hsv
    
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
    
    

reds = HSVColorRange(HSVColor(0, 0, 0), HSVColor(179, 255, 255))
red_trackbar = HSVTrackbar("Red", reds.lower, reds.upper)

blues = HSVColorRange(HSVColor(0, 0, 0), HSVColor(179, 255, 255))
blue_trackbar = HSVTrackbar("Blue", blues.lower, blues.upper)


while True:
    ret, frame = vs.read()
    frame = imutils.resize(frame, width=400)
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    red_mask = cv2.inRange(hsv, reds.lower.hsv, reds.upper.hsv)
    red_mask = cv2.erode(red_mask, None, iterations=2) # type: ignore
    red_mask = cv2.dilate(red_mask, None, iterations=2) # type: ignore

    

    

    cnts = cv2.findContours(red_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # draw the contours on the frame

    filtered_cnts = [c for c in cnts if cv2.contourArea(c) > 300]

    cv2.drawContours(frame, filtered_cnts, -1, (255, 0, 0), 3)
    center = None

    for c in filtered_cnts:
        M = cv2.moments(c)
        if M["m00"] > 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cv2.circle(frame, center, 5, (0, 255, 0), -1)
            # reactangle around the contour
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Red", (int(center[0]), int(center[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0, 0, 0], 2)


    



    blue_mask = cv2.inRange(hsv, blues.lower.hsv, blues.upper.hsv)
    blue_mask = cv2.erode(blue_mask, None, iterations=2) # type: ignore
    blue_mask = cv2.dilate(blue_mask, None, iterations=2) # type: ignore

    cnts = cv2.findContours(blue_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # draw the contours on the frame

    filtered_cnts = [c for c in cnts if cv2.contourArea(c) > 300]

    cv2.drawContours(frame, filtered_cnts, -1, (255, 0, 0), 3)
    center = None

    for c in filtered_cnts:
        M = cv2.moments(c)
        if M["m00"] > 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cv2.circle(frame, center, 5, (0, 255, 0), -1)
            # reactangle around the contour
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Blue", (int(center[0]), int(center[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0, 0, 0], 2)

    cv2.imshow("Red Mask", red_mask)
    cv2.imshow("Blue Mask", blue_mask)
    cv2.imshow("Frame", frame)
    # show some sliders to tune lower red and upper red

    

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


cv2.destroyAllWindows()

