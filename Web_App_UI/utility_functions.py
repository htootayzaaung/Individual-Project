import cv2
import numpy as np

DETECTRON2_CLASS_NAMES = ["Axe", "Gun", "Knife"]

# Constants for standardization
STANDARD_BORDER_THICKNESS = 2  # Consistent border thickness
STANDARD_FONT_STYLE = cv2.FONT_HERSHEY_DUPLEX  # Consistent font style
STANDARD_FONT_SIZE = 1  # Consistent font size
TEXT_COLOR = (255, 255, 255)  # White text color

# Predefined class-specific colors
CLASS_COLORS = {
    "Axe": (9, 180, 105),  # Green
    "Gun": (255, 81, 31),  # Blue
    "Knife": (49, 49, 255)  # Red
}

# Function to draw text label with a background, ensuring proper alignment with the bounding box
def draw_label_with_background(frame, label, position, class_name):
    class_color = CLASS_COLORS[class_name]  # Use class-specific color

    # Calculate text size and adjust the position to reduce the gap
    text_size = cv2.getTextSize(label, STANDARD_FONT_STYLE, STANDARD_FONT_SIZE, STANDARD_BORDER_THICKNESS)[0]

    # Adjust the filled rectangle position to minimize the gap
    rectangle_top_left = (position[0], position[1] - text_size[1])  # Aligns closely with bounding box
    rectangle_bottom_right = (position[0] + text_size[0], position[1] - 1)  # -1 to bring it close to the box edge

    # Draw filled rectangle for the label's background
    cv2.rectangle(frame, rectangle_top_left, rectangle_bottom_right, class_color, -1)

    # Draw the text label, ensuring proper alignment
    cv2.putText(frame, label, (position[0], rectangle_top_left[1] + text_size[1]), STANDARD_FONT_STYLE, STANDARD_FONT_SIZE, TEXT_COLOR, STANDARD_BORDER_THICKNESS)


def overlay(image, mask, color, alpha, resize=None):
    colored_mask = np.expand_dims(mask, 0).repeat(3, axis=0)
    colored_mask = np.moveaxis(colored_mask, 0, -1)
    masked = np.ma.MaskedArray(image, mask=colored_mask, fill_value=color)
    image_overlay = masked.filled()

    if resize is not None:
        image = cv2.resize(image.transpose(1, 2, 0), resize)
        image_overlay = cv2.resize(image_overlay.transpose(1, 2, 0), resize)

    image_combined = cv2.addWeighted(image, 1 - alpha, image_overlay, alpha, 0)

    return image_combined

def plot_one_box(x, img, color=None, label=None, line_thickness=3):
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    if color is None:
        return
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
        
def correct_coordinates(x1, x2, y1, y2):
    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)
    return x1, x2, y1, y2
    