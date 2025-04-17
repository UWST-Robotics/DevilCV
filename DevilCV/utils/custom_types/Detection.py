from typing import Callable, List
from pydantic import BaseModel
import cv2.typing

type Center = tuple[int, int]
class Detection(BaseModel):
    bounding_box: cv2.typing.Rect
    center: Center
type CenterDetection = dict[str, dict[str, List[Center]]]
type Detections = dict[str, List[Detection]]
type CenterCallback = Callable[[Detections], None]
