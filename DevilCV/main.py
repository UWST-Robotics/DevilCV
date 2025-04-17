from DevilCV.Vision.Stream import Stream
from DevilCV.Vision.Detection.MultiColorDetector import MultiColorDetector
from DevilCV.utils.custom_types.Color import HSVColorRange, HSVColor
from DevilCV.utils.custom_types.Detection import Detections

def main():
    # Define color ranges for detection
    color_ranges = [
        HSVColorRange(HSVColor(0, 87, 123), HSVColor(12, 255, 215)),
        # blue
        HSVColorRange(HSVColor(110, 50, 50), HSVColor(130, 255, 255)),
    ]

    detector_names = ["Red", "Blue"]
    multi_detector = MultiColorDetector(color_ranges, detector_names, 1000)

    stream = Stream(source=0, exposure=-4, multi_detectors=[multi_detector], show=True)

    def callback(center_detections: Detections):
        print(center_detections)

    stream.start(callback)

if __name__ == "__main__":
    main()