from abc import ABC, abstractmethod
from typing import List, Sequence
import cv2.typing
from DevilCV.utils.custom_types.Detection import Detection

Contours = Sequence[cv2.typing.MatLike]
Mask = cv2.typing.MatLike
Center = tuple[int, int]

class Detector(ABC):
    name: str
    
    @abstractmethod
    def centers(self, contours) -> Sequence[Center]:
        pass

    def mask(self, hsv_frame: cv2.typing.MatLike) -> tuple[Contours, Mask]:
        # not implemented in base class
        raise NotImplementedError("This method should be overridden in a subclass")
    
    def detect(self, hsv_frame: cv2.typing.MatLike) -> Sequence[Detection]:
        raise NotImplementedError("This method should be overridden in a subclass")
    
class MultiDetector(ABC):
    name: str
    @abstractmethod
    def multimask(self, hsv_frame: cv2.typing.MatLike) -> tuple[dict[str, Contours], dict[str, Mask]]:
        raise NotImplementedError("This method should be overridden in a subclass")

    @abstractmethod
    def multicenters(self, contours: dict[str, Contours]) -> dict[str, Sequence[Center]]:
        raise NotImplementedError("This method should be overridden in a subclass")

    def multidetect(self, hsv_frame: cv2.typing.MatLike) -> dict[str, Sequence[Detection]]:
        raise NotImplementedError("This method should be overridden in a subclass")
    