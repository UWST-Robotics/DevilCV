from DevilCV.Vision.Stream import Stream
from DevilCV.Vision.Detection.MultiColorDetector import MultiColorDetector
from DevilCV.utils.custom_types.Color import HSVColorRange, HSVColor
from DevilCV.utils.custom_types.Detection import Detections

def main():

    detectors = {
        "Red": [HSVColorRange(HSVColor(160, 100, 100), HSVColor(179, 255, 255)), HSVColorRange(HSVColor(0, 100, 100), HSVColor(20, 255, 255))],
        "Blue": [HSVColorRange(HSVColor(100, 100, 92), HSVColor(124, 255, 255))],
    }

    multi_detector = MultiColorDetector(detectors, 1000)

    stream = Stream(source=0, exposure=-6, multi_detectors=[multi_detector], show=True)

    def callback(center_detections: Detections):
        print(center_detections)

    stream.start(callback, record=True)

if __name__ == "__main__":
    main()