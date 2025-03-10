from PIL import Image, ImageDraw, ImageFont
import textwrap
from io import BytesIO    
import base64

def draw_text(draw, text, x, y, width, font_size, font_name, multiline=False):
    scale = 1
    x *= scale
    y *= scale
    width *= scale
    font_size *= scale

    # Font paths
    font = {
        "bold": "fonts\GoogleSans-Bold.ttf",
        "bold_italic": "fonts\GoogleSans-BoldItalic.ttf",
        "italic": "fonts\GoogleSans-Italic.ttf",
        "medium": "fonts\GoogleSans-Medium.ttf",
        "medium_italic": "fonts\GoogleSans-MediumItalic.ttf",
        "regular": "fonts\GoogleSans-Regular.ttf"
    }

    font = ImageFont.truetype(r"C:\Users\oxyje\Downloads\GoogleSans-Regular.ttf", font_size)

    if multiline:
        # Wrap text to fit within the given width
        max_line_char = width // (font_size // 2) # Based on the assumption that the width of a character is half of its height
        wrapped_text = textwrap.fill(text, width=max_line_char)
        lines = wrapped_text.split("\n")
        line_height = font_size + 5 # Fixed for now, adjust later?

        for i, line in enumerate(lines):
            text_bbox = draw.textbbox((0,0), line, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            x_centered = x + (width - text_width) // 2
            draw.text((x_centered, y + i * line_height), line, font=font, fill=(255,255,255))
    else:
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        x_centered = x + (width - text_width) // 2
        draw.text((x_centered, y), text, font=font, fill=(255, 255, 255))


def image_url(img):
    """
    Converts a PIL image to a base64 encoded string and returns a data URL.
    """
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"
