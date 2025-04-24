def top_left_to_center(x: int, y: int, resolution: tuple[int, int]) -> tuple[int, int]:
    """
    Convert top-left coordinates to center coordinates.
    
    Args:
        x (int): The x-coordinate of the top-left corner.
        y (int): The y-coordinate of the top-left corner.
        resolution (tuple[int, int]): The resolution of the image (width, height).
        
    Returns:
        tuple[int, int]: The center coordinates (x, y).
    """
    return (x + resolution[0] // 2, y + resolution[1] // 2)

def center_to_relative(center: tuple[int, int], resolution: tuple[int, int]) -> tuple[float, float]:
    """
    Convert center coordinates to relative coordinates.
    
    Args:
        center (tuple[int, int]): The center coordinates (x, y).
        resolution (tuple[int, int]): The resolution of the image (width, height).
        
    Returns:
        tuple[float, float]: The relative coordinates (x, y).
    """
    return (center[0] / resolution[0], center[1] / resolution[1])

def top_left_to_center_relative(x: int, y: int, resolution: tuple[int, int]) -> tuple[float, float]:
    """
    Convert top-left coordinates to relative center coordinates.
    
    Args:
        x (int): The x-coordinate of the top-left corner.
        y (int): The y-coordinate of the top-left corner.
        resolution (tuple[int, int]): The resolution of the image (width, height).
        
    Returns:
        tuple[float, float]: The relative center coordinates (x, y).
    """
    center = top_left_to_center(x, y, resolution)
    return center_to_relative(center, resolution)