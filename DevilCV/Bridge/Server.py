from flask import Flask, request, jsonify
from DevilCV.utils.custom_types.Color import HSVColorRange, HSVColor
from DevilCV.Vision.Detection.Detector import MultiDetector


class Server:
    def __init__(self, host: str = "localhost", port: int = 5000):
        self.host = host
        self.port = port

    def start(self, color_detector: MultiDetector):
        app = Flask(__name__)

        names = [detector.name for detector in color_detector.detectors]

        @app.route('/names', methods=['GET'])
        def get_detectors():
            return jsonify(names), 200

        @app.post('/change')
        def change_detectors():
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid data"}), 400

            for name, ranges in data.items():
                

                # check all ranges are valid
                for i, range in enumerate(ranges):
                    if not isinstance(range, dict) or 'lower' not in range or 'upper' not in range:
                        return jsonify({"error": f"Invalid range format for {name}"}), 400

                    lower = range['lower']
                    upper = range['upper']

                    if not all(k in lower for k in ('h', 's', 'v')) or not all(k in upper for k in ('h', 's', 'v')):
                        return jsonify({"error": f"Invalid HSV values for {name}"}), 400

                    
                    lower_hsv = HSVColor(lower['h'], lower['s'], lower['v'])
                    upper_hsv = HSVColor(upper['h'], upper['s'], upper['v'])
                    ranges[i] = HSVColorRange(lower_hsv, upper_hsv)

                # update the color range for the detector
                color_detector.multiupdate_color(name, ranges)
            
            return jsonify({"message": "Detectors updated successfully"}), 200
        

        app.run(host=self.host, port=self.port)

    