from typing import Callable, List, Mapping
from pydantic import BaseModel
import cv2.typing

Center = tuple[int, int]
class Detection(BaseModel):
    bounding_box: cv2.typing.Rect
    center: Center
Detections = Mapping[str, Mapping[str, List[Detection]]]
CenterCallback = Callable[[Detections], None]
