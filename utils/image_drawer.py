from PIL import Image, ImageDraw, ImageFont
import textwrap


def draw_text(draw, text, x, y, width, font_size, font_name, scale, multiline=False):
    x *= scale
    y *= scale
    width *= scale
    font_size *= scale

    # Font paths
    font = {
        "bold": r"static\fonts\GoogleSans-Bold.ttf",
        "bold_italic": r"static\fonts\GoogleSans-BoldItalic.ttf",
        "italic": r"static\fonts\GoogleSans-Italic.ttf",
        "medium": r"static\fonts\GoogleSans-Medium.ttf",
        "medium_italic": r"static\fonts\GoogleSans-MediumItalic.ttf",
        "regular": r"static\fonts\GoogleSans-Regular.ttf"
    }

    font = ImageFont.truetype(font[font_name], font_size)

    if multiline:
        # Wrap text to fit within the given width
        max_line_char = width // (font_size // 2) # Based on the assumption that the width of a character is half of its height
        wrapped_text = textwrap.fill(text, width=max_line_char)
        lines = wrapped_text.split("\n")
        line_height = font_size + 5 

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

    
def cert_maker(participant_name, event_type, event_title, department, event_description, event_date, gdg_lead, lead_name, colead_name):
    # Load the template
    img = Image.open(r"static\images\template_certificate.png").convert("RGB")

    # Create a draw object to the template
    draw = ImageDraw.Draw(img)

    # Position can be derived from Figma
    draw_text(draw, participant_name, 85, 258, 623, 48, "bold", 4, multiline=False)
    draw_text(draw, "has successfully participated in the " + event_type, 200, 356, 402, 12, "medium", 4, multiline=False)
    draw_text(draw, event_title, 6, 379, 780, 20, "bold", 4, multiline=False)
    draw_text(draw, "organized by the " + department, 256, 411, 282, 12, "medium", 4, multiline=False)
    draw_text(draw, event_description, 136, 437, 520, 10, "medium", 4, multiline=True)
    draw_text(draw, "Awarded on " + event_date, 296, 487, 201, 13, "medium", 4, multiline=False)
    draw_text(draw,  gdg_lead, 154, 534, 133, 13, "bold", 4, multiline=False)
    draw_text(draw,  "GDG PUP President and Chapter Lead" , 170, 550, 102, 8, "medium", 4, multiline=True)
    draw_text(draw,  lead_name, 292, 537, 198, 13, "bold", 4, multiline=False)
    draw_text(draw,  "GDG PUP " + "Cybersecurity " + "Lead", 336.55, 555.96, 107.91, 8, "medium", 4, multiline=False)
    draw_text(draw,  colead_name, 501, 537, 121, 13, "bold", 4, multiline=False)
    draw_text(draw,  "GDG PUP " + "Cybersecurity " + "Co-Lead", 500, 554, 122, 8, "medium", 4, multiline=False)

    # Return the image
    return img