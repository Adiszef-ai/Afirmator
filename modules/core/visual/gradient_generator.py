"""
Moduł do generowania gradientów dla wizualnych cytatów
"""
from PIL import Image

def create_gradient_background(width, height, color1, color2, direction="vertical"):
    """
    Tworzy tło gradientowe.
    
    Args:
        width (int): Szerokość obrazu
        height (int): Wysokość obrazu
        color1 (tuple): Pierwszy kolor RGB
        color2 (tuple): Drugi kolor RGB
        direction (str): Kierunek gradientu ("vertical", "horizontal", "diagonal_tl_br", "diagonal_tr_bl", "radial")
    
    Returns:
        Image: Obraz z gradientem
    """
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    
    for y in range(height):
        for x in range(width):
            if direction == "vertical":
                value = int(255 * (y / height))
            elif direction == "horizontal":
                value = int(255 * (x / width))
            elif direction == "diagonal_tl_br":
                value = int(255 * ((x / width + y / height) / 2))
            elif direction == "diagonal_tr_bl":
                value = int(255 * ((1 - x / width + y / height) / 2))
            elif direction == "radial":
                center_x, center_y = width / 2, height / 2
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                max_distance = ((width / 2) ** 2 + (height / 2) ** 2) ** 0.5
                value = int(255 * min(1.0, distance / max_distance))
            else:
                value = int(255 * (y / height))
            mask_data.append(value)
    
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base