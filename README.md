# DevilCV: Computer Vision service for VEXBridge

DevilCV is a computer vision service for VEXBridge. It provides an interface to detect colors using OpenCV and send them to the Bridge.

## Detection 

The detection data sent to VEXBridge is made up of a center (`center_x`) and an edge (`edge_x`).

The full detection type definition is as follows:
```python
class Detection(BaseModel):
    bounding_box: cv2.typing.Rect # tuple of (x, y, w, h)
    center: Center
```

### Meaning of detection values

Detection values represent relative positions of the detected object from the center of the camera, where the center is `1`, the leftmost point is `0.5` (meaning 50% of the way to the center), and the rightmost point is `1.5` (meaning 50% over the center).  

## Value Paths

Paths always start with `vision`, followed by the detection type, then class type, and finally the variable name. For example, a red color detector will have paths `vision/color/red/center_x` and `vision/color/red/edge_x`. 