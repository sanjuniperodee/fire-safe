import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
from datetime import datetime
import requests
import urllib3
import math

from objects.models import SubBuilding, BuildingImage, SubBuildingImage, BuildingPDFDocument

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BuildingPDFGenerator:
    def __init__(self, building):
        self.building = building
        self.width, self.height = A4

        # Register DejaVuSerif font for Cyrillic support
        font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'DejaVuSerif.ttf')
        font_path_bold = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'DejaVuSerif.ttf')
        try:
            pdfmetrics.registerFont(TTFont('DejaVuSerif', font_path))
            pdfmetrics.registerFont(TTFont('DejaVuSerif-Bold', font_path_bold))
            self.font_name = 'DejaVuSerif'
            self.font_name_bold = 'DejaVuSerif'
        except:
            print("Could not load DejaVuSerif font, falling back to Helvetica")
            self.font_name = 'Helvetica'
            self.font_name_bold = 'Helvetica'

    # def get_image_from_url(self, image_file):
    #     """Get image from URL and return as PIL Image object."""
    #     try:
    #         # Get image URL
    #         image_url = image_file.url
    #
    #         # Download image content
    #         response = requests.get(image_url, verify=False)
    #         response.raise_for_status()
    #
    #         # print(response.content)
    #
    #         # Create PIL Image from content
    #         img_data = BytesIO(response.content)
    #         return Image.open(img_data)
    #     except Exception as e:
    #         print(f"Error loading image: {e}")
    #         return None
    def get_image_from_url(self, image_file):
        """Get image from URL and return as PIL Image object."""
        try:
            # Get image URL
            image_url = image_file.url

            # Download image content
            response = requests.get(image_url, verify=False)
            response.raise_for_status()

            # Create PIL Image from content
            img_data = BytesIO(response.content)
            img = Image.open(img_data)

            # Get EXIF orientation if it exists
            try:
                exif = img._getexif()
                if exif is not None:
                    orientation = exif.get(274)  # 274 is the orientation tag
                    if orientation is not None:
                        # Rotate or flip the image according to EXIF orientation
                        if orientation == 3:
                            img = img.rotate(180, expand=True)
                        elif orientation == 6:
                            img = img.rotate(270, expand=True)
                        elif orientation == 8:
                            img = img.rotate(90, expand=True)
            except (AttributeError, KeyError, IndexError):
                # No EXIF data or no orientation tag
                pass

            # Convert to RGB if necessary (handles RGBA images)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            return img

        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def draw_image_in_box(self, p, image_file, x, y, box_width, box_height):
        try:
            # Get image from URL
            img = self.get_image_from_url(image_file)
            if img is None:
                raise Exception("Could not load image")

            # Calculate aspect ratio
            aspect = img.width / img.height

            # Calculate dimensions to fit in box while maintaining aspect ratio
            if aspect > box_width / box_height:  # wider than box
                new_width = box_width
                new_height = box_width / aspect
            else:  # taller than box
                new_height = box_height
                new_width = box_height * aspect

            # Center the image in the box
            x_offset = (box_width - new_width) / 2
            y_offset = (box_height - new_height) / 2

            x_image_right = x + x_offset + new_width
            x_image_left = x+x_offset

            y_image_top = y+y_offset+new_height
            y_image_bottom = y+y_offset

            # Draw the image
            p.drawImage(ImageReader(img),
                        x + x_offset,
                        y + y_offset,
                        # 120,
                        # 600,
                        width=new_width,
                        height=new_height)

            # Close PIL Image
            img.close()
            x_image_left = x
            return x_image_left, x_image_right, y_image_top, y_image_bottom

        except Exception as e:
            # If image can't be loaded, draw placeholder text
            p.rect(x, y, box_width, box_height)
            p.drawString(x + 5 * mm, y + box_height / 2, "ФОТО")

            x_image_left = x
            x_image_right = x + box_width

            y_image_top = y
            y_image_bottom = y + box_height
            return x_image_left, x_image_right, y_image_top, y_image_bottom

    def wrap_text(self, p, text, x_start, available_width):
        """
        Splits text into lines that fit within available_width.
        Returns list of lines and total height needed.
        """
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            # Try adding new word to current line
            test_line = ' '.join(current_line + [word])
            width = p.stringWidth(test_line, self.font_name, 12)

            if width <= available_width:
                current_line.append(word)
            else:
                # Start new line if current one would be too wide
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        # Add last line
        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def draw_wrapped_text(self, p, text, x, y, available_width):
        """
        Draws text with word wrapping and returns the new y position.
        Uses a more restricted width and improved line spacing.
        """
        # Ограничиваем максимальную ширину текста до разумного значения
        max_width = 150 * mm  # максимальная ширина текста
        actual_width = min(available_width, max_width)

        # Разбиваем текст на части по 100 символов для предварительной обработки
        # text_chunks = [text[i:i + 100] for i in range(0, len(text), 100)]
        text_chunks = [text[i:i + 300] for i in range(0, len(text), 300)]
        lines = []

        for chunk in text_chunks:
            words = chunk.split()
            current_line = []
            current_width = 0

            for word in words:
                # word_width = p.stringWidth(word + ' ', self.font_name, 12)
                word_width = p.stringWidth(word + ' ', self.font_name, 10)
                if current_width + word_width <= actual_width:
                    current_line.append(word)
                    current_width += word_width
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
                    current_width = word_width

            if current_line:
                lines.append(' '.join(current_line))

        # Отрисовка строк с увеличенным межстрочным интервалом
        line_height = 6 * mm  # Увеличенный интервал между строками
        current_y = y
        for line in lines:
            p.drawString(x, current_y, line)
            current_y -= line_height
        return current_y

    def get_formatted_list_values(self, queryset, field_name):
        """
        Helper method to format values from a queryset's ManyToMany field.

        Args:
            queryset: QuerySet containing the related objects
            field_name: String name of the field for printing

        Returns:
            tuple: (formatted_text, debug_message)
        """
        values_list = list(queryset.values_list('name', flat=True))
        formatted_text = ', '.join(values_list) if values_list else 'Не указан'
        debug_message = f'{field_name}: {formatted_text}'
        return formatted_text, debug_message

    def draw_labeled_text(self, p, label, value, x_start, y_position, available_width=100 * mm, font_size=8):
        """
        Draws a label followed by wrapped text value and returns the new y position.

        Args:
            p: Canvas object
            label: String label to draw
            value: String value to draw after label
            x_start: Starting x position
            y_position: Starting y position
            available_width: Available width for the text (defaults to 100mm)

        Returns:
            float: New y position after drawing text
        """
        # label = Характеристика подздания
        # Calculate label width
        label_width = p.stringWidth(label, self.font_name, font_size)
        # Calculate positions
        label_x = x_start
        text_x = x_start + label_width + 1 * mm  # Add 2mm spacing after label
        # Draw the label
        p.drawString(label_x, y_position, label)
        # Draw the wrapped value and get new y position
        value_text = str(value or 'Не указан')
        # Draw wrapped text and get new y position
        new_y = self.draw_wrapped_text(
            p,
            value_text,
            text_x,
            y_position,
            available_width
        )
        # Add additional spacing after the text block
        return new_y    # - 10 * mm

    def draw_field_with_label(self, p, label, queryset, field_name, x_image_left, y_image_bottom,
                              available_width=200 * mm):
        """
        Helper method to draw a labeled field with values from a queryset.

        Args:
            p: Canvas object
            label: Label to display
            queryset: QuerySet containing the related objects
            field_name: Name of the field for debugging
            x_image_left: X coordinate
            y_image_bottom: Y coordinate
            available_width: Available width for text

        Returns:
            float: New y position after drawing
        """
        formatted_text, debug_message = self.get_formatted_list_values(queryset, field_name)
        return self.draw_labeled_text(
            p,
            label,
            formatted_text,
            x_image_left,
            y_image_bottom,
            available_width=available_width
        )

    def check_and_create_new_page(self, p, y_position, required_space=30 * mm, font_size=8):
        """
        Check if there's enough space on the current page, if not create a new one.

        Args:
            p: Canvas object
            y_position: Current y position
            required_space: Minimum space needed for next content block (default 30mm)

        Returns:
            float: New y position
        """
        # Define minimum margin at bottom of page
        bottom_margin = 20 * mm

        # If we're too close to bottom of page
        if y_position < bottom_margin + required_space:
            # Create new page
            p.showPage()
            # Reset font and position for new page
            p.setFont(self.font_name, font_size)
            return 270 * mm  # Start from top of new page
        return y_position

    def add_seal_to_pdf(self, p, x, y, size=100):
        """Adds the template seal image to PDF and overlays the text"""
        try:
            # Load the template seal image
            template_path = os.path.join(settings.BASE_DIR, 'static', 'seal_template', 'Building_Seal.png')
            template = Image.open(template_path)

            # Create a copy to work with
            seal = template.copy()
            draw = ImageDraw.Draw(seal)

            # Load font for Cyrillic text
            try:
                font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'DejaVuSerif.ttf')
                circle_font = ImageFont.truetype(font_path, size=30) # 40  # Adjust size as needed
                center_font = ImageFont.truetype(font_path, size=45)  # Adjust size as needed
            except:
                print("Could not load DejaVuSerif font, falling back to default")
                circle_font = ImageFont.load_default()
                center_font = ImageFont.load_default()

            # Get image dimensions
            width, height = seal.size
            center_x = width // 2
            center_y = height // 2
            radius = float(min(width, height)) // 2.6  # Radius for text placement

            # Add organization name in curved pattern
            organization_name = self.building.organization_name or "НАИМЕНОВАНИЕ"

            if len(organization_name) > 10:
                font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'DejaVuSerif.ttf')
                circle_font = ImageFont.truetype(font_path, size=15)  # 40  # Adjust size as needed

            # Calculate total text width to distribute letters evenly
            total_width = sum(draw.textlength(char, font=circle_font) for char in organization_name)

            # Calculate the arc's starting and ending angles (in radians)
            start_angle = math.pi + math.pi/6  # Start at top (180 degrees)
            angle_span = -math.pi  # Span 180 degrees

            # Draw each character rotated along the arc
            current_angle = start_angle
            x_pos = 0

            for char in organization_name:
                # Calculate character width
                char_width = draw.textlength(char, font=circle_font)

                # Calculate position on the arc
                angle = current_angle - (angle_span * x_pos / total_width)

                # Calculate position
                char_x = center_x + radius * math.cos(angle)
                char_y = center_y + radius * math.sin(angle)

                # Calculate rotation angle (tangent to the circle)
                rotation_angle = math.degrees(angle) + 180

                # Draw the rotated character
                draw.text(
                    (char_x, char_y),
                    char,
                    font=circle_font,
                    fill='rgb(41, 98, 255)',
                    anchor="mm",
                    angle=rotation_angle
                )

                x_pos += char_width

            # Add IIN/БИН in center
            iin_text = f"{self.building.iin}"
            # Calculate text dimensions for IIN
            font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'DejaVuSerif.ttf')
            center_font = ImageFont.truetype(font_path, size=20)
            bbox = draw.textbbox((0, 0), iin_text, font=center_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Draw IIN text in center
            draw.text(
                (center_x - text_width / 2.8, center_y - text_height / 1),
                iin_text,
                font=center_font,
                fill='rgb(41, 98, 255)'  # Match template blue color
            )

            # Save the modified seal to bytes for PDF
            seal_bytes = BytesIO()
            seal.save(seal_bytes, format='PNG')
            seal_bytes.seek(0)

            # Draw on PDF
            p.drawImage(
                ImageReader(seal_bytes),
                x - size / 2,
                y - size / 2,
                width=size,
                height=size,
                mask='auto'  # For transparent background
            )

            # Cleanup
            seal_bytes.close()
            template.close()
            seal.close()

        except Exception as e:
            print(f"Error adding seal: {e}")
            # Draw placeholder if seal fails
            p.circle(x, y, size / 2)
            p.drawString(x - 20, y, "ПЕЧАТЬ")

    def generate_and_save(self):
        buffer = BytesIO()

        # Create PDF object
        p = canvas.Canvas(buffer, pagesize=A4)

        # Set font for title
        p.setFont(f"{self.font_name_bold}", 14)
        # p.setFont(f"{self.font_name}", 14) # 16
        p.drawString(50 * mm, 270 * mm, "ПАСПОРТ ПОЖАРНОЙ БЕЗОПАСНОСТИ")
        p.setFont(f"{self.font_name}", 10)
        # Draw main building image if exists
        y = 230 * mm
        building_image = BuildingImage.objects.filter(building=self.building).first()
        if building_image:
            x_image_left, x_image_right, y_image_top, y_image_bottom = self.draw_image_in_box(p,
                                   building_image.image,
                                   20 * mm, y - 30 * mm,
                                   80 * mm, 60 * mm)
        else:
            p.rect(20 * mm, y - 30 * mm, 80 * mm, 60 * mm)
            p.drawString(35 * mm, y - 5 * mm, "ФОТО ОТСУТСТВУЕТ")
            x_image_right = 100 * mm
            y_image_top = y + 30 * mm

            x_image_left = 20 * mm
            y_image_bottom = y - 30 * mm

        x_image_right_old = x_image_right
        # Building Information
        y_image_top -= 5 * mm
        # p.drawString(x_image_right + 10 * mm, y_image_top, "Наименование: {}".format(
        #     self.building.organization_name or 'string'))
        # Handle organization name with wrapping
        org_name = "Наименование: {}".format(self.building.organization_name or 'string')
        wrapped_lines = self.wrap_text(p, org_name, x_image_right + 10 * mm, 80 * mm)  # Limit width to 80mm
        for line in wrapped_lines:
            p.drawString(x_image_right + 10 * mm, y_image_top, line)
            y_image_top -= 7 * mm  # Adjust spacing between wrapped lines
        # y_image_top -= 10 * mm
        # y_image_top -= 7 * mm
        p.drawString(x_image_right + 10 * mm, y_image_top, "ИИН/БИН: {}".format(self.building.iin))
        y_image_top -= 7 * mm
        p.drawString(x_image_right + 10 * mm, y_image_top, "Контактный Телефон: {}".format(self.building.owner.phone))

        # SubBuilding Information
        p.setFont(self.font_name, 9)  # 12
        subbuildings = SubBuilding.objects.filter(building=self.building)
        # x_image_right = x_image_right + 26 * mm
        x_image_right = self.width / 2
        # x_image_right += 6 * mm
        if subbuildings:
            p.setLineWidth(.3)
            p.line(x_image_left, y_image_bottom - 5 * mm, x_image_right * 1.8, y_image_bottom - 5 * mm)
            for subbuilding in subbuildings:
                # Check if we need a new page for the subbuilding header
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom)

                y_image_bottom -= 10 * mm

                p.drawString(x_image_left, y_image_bottom, "Название: {}".format(
                    subbuilding.title or 'Не заполнено'))
                y_image_bottom -= 6 * mm
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom)

                p.drawString(x_image_left, y_image_bottom, "Объект Организации: {}".format(
                    subbuilding.subbuilding_type or 'Не указан'))
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom)

                if subbuilding.subbuilding_optional_subtype_type:
                    # p.drawString(x_image_right, y_image_bottom, "Тип подздания: {}".format(
                    #     subbuilding.subbuilding_optional_subtype_type))
                    y_image_bottom = self.draw_labeled_text(
                        p,
                        "Тип подздания:",
                        subbuilding.subbuilding_optional_subtype_type,
                        x_image_right,
                        y_image_bottom,
                        available_width=50 * mm,
                        font_size=9,
                    )
                else:
                    y_image_bottom -= 6 * mm
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom)

                # p.drawString(x_image_left, y_image_bottom, "Под тип Здания: {}".format(
                #     subbuilding.subbuilding_subtype or 'Не указан'))
                y_image_bottom_old = y_image_bottom
                y_image_bottom = self.draw_labeled_text(
                    p,
                    "Под тип Здания:",
                    subbuilding.subbuilding_subtype,
                    x_image_left,
                    y_image_bottom,
                    available_width=50 * mm,
                    font_size=9,
                )
                y_image_bottom_left = y_image_bottom
                # p.drawString(x_image_right, y_image_bottom, "Предназначение: {}".format(
                #     subbuilding.functional_purpose or 'Не заполнен'))
                # y_image_bottom -= 6 * mm
                y_image_bottom = self.draw_labeled_text(
                    p,
                    "Предназначение:",
                    subbuilding.functional_purpose,
                    x_image_right,
                    y_image_bottom_old,
                    available_width=50 * mm,
                    font_size=9,
                )
                y_image_bottom = min(y_image_bottom_left, y_image_bottom)
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom)

                p.setFont(self.font_name, 8)  # 12
                y_image_bottom_old = y_image_bottom
                y_image_bottom = self.draw_labeled_text(
                    p,
                    "Характеристика подздания:",
                    subbuilding.subbuilding_characteristics,
                    x_image_left,
                    y_image_bottom,
                    available_width=50 * mm,
                )
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom)
                # print(f'y_image_bottom: {y_image_bottom}, y_image_bottom_old: {y_image_bottom_old}')
                p.drawString(x_image_right, y_image_bottom_old, "Класс конструктивной ПО: {}".format(
                    subbuilding.structural_po_class or 'Отсутствует'))
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom)
                # y_image_bottom -= 10 * mm

                p.drawString(x_image_left, y_image_bottom, "Дата постройки/реконструкции: {}".format(
                    subbuilding.year_construction_reconstruction))
                p.drawString(x_image_right, y_image_bottom, "Дата Ввода в эксплуатацию: {}".format(
                    subbuilding.date_commissioning.strftime('%d.%m.%Y')))
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom)
                y_image_bottom -= 6 * mm

                p.drawString(x_image_left, y_image_bottom, "Рейтинг: {}".format(
                    subbuilding.rating or 'Отсутствует'))
                p.drawString(x_image_right, y_image_bottom, "Высота: {} м".format(
                    subbuilding.building_height or 'Не указан'))
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom)
                y_image_bottom -= 6 * mm

                p.drawString(x_image_left, y_image_bottom, "Всего этажей: {}".format(
                    subbuilding.total_floors or 'Не указан'))
                p.drawString(x_image_right, y_image_bottom, "Площадь: {} м^2".format(
                    subbuilding.area or 'Не указан'))
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom)
                y_image_bottom -= 6 * mm

                p.drawString(x_image_left, y_image_bottom, "Этаж: {}".format(
                    subbuilding.floor_number or 'Не указан'))
                p.drawString(x_image_right, y_image_bottom, "Объем: {} м^3".format(
                    subbuilding.volume or 'Не указан'))
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom)
                y_image_bottom -= 6 * mm

                # Внутренние стены и перегородки
                y_image_bottom_old = y_image_bottom
                y_image_bottom = self.draw_field_with_label(
                    p,
                    "Внутренние стены и перегородки:",
                    subbuilding.inner_walls_material,
                    "Внутренние стены и перегородки:",
                    x_image_left,
                    y_image_bottom,
                    available_width=40 * mm,
                )
                y_image_bottom_left = y_image_bottom

                # Типы кровли
                y_image_bottom = self.draw_field_with_label(
                    p,
                    "Тип кровли:",
                    subbuilding.roof,
                    "Тип кровли",
                    x_image_right,
                    y_image_bottom_old,
                    available_width=80 * mm,
                )
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom)
                y_image_bottom = min(y_image_bottom_left, y_image_bottom)

                # Типы лестницы
                y_image_bottom_old = y_image_bottom
                y_image_bottom = self.draw_field_with_label(
                    p,
                    "Тип лестницы:",
                    subbuilding.stairs_type,
                    "Тип лестницы",
                    x_image_left,
                    y_image_bottom,
                    available_width=80 * mm,
                )
                y_image_bottom_left = y_image_bottom

                # Материал лестницы
                y_image_bottom = self.draw_field_with_label(
                    p,
                    "Материал лестницы:",
                    subbuilding.stairs_material,
                    "Материал лестницы",
                    x_image_right,
                    y_image_bottom_old,
                    available_width=60 * mm,
                )
                y_image_bottom = min(y_image_bottom_left, y_image_bottom)
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom)

                # Освещение
                y_image_bottom_old = y_image_bottom
                y_image_bottom = self.draw_field_with_label(
                    p,
                    "Освещение:",
                    subbuilding.lighting,
                    "Освещение",
                    x_image_left,
                    y_image_bottom,
                    available_width=60 * mm,
                )
                y_image_bottom_left = y_image_bottom

                # Вентиляция
                y_image_bottom = self.draw_field_with_label(
                    p,
                    "Вентиляция:",
                    subbuilding.ventilation,
                    "Вентиляция",
                    x_image_right,
                    y_image_bottom_old,
                    # available_width=60 * mm,
                    available_width=80 * mm,
                )
                y_image_bottom = min(y_image_bottom_left, y_image_bottom)
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom)

                # Отопление
                y_image_bottom_old = y_image_bottom
                y_image_bottom = self.draw_field_with_label(
                    p,
                    "Отопление:",
                    subbuilding.heating,
                    "Отопление",
                    x_image_left,
                    y_image_bottom,
                    # available_width=45 * mm,
                    available_width=80 * mm,
                )
                y_image_bottom_left = y_image_bottom

                # Объект охраняется
                y_image_bottom = self.draw_field_with_label(
                    p,
                    "Объект охраняется:",
                    subbuilding.security,
                    "Объект охраняется",
                    x_image_right,
                    y_image_bottom_old,
                    available_width=80 * mm,
                )
                y_image_bottom = min(y_image_bottom_left, y_image_bottom)
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom)

                # Аварийное освещение (Имеется)
                p.drawString(x_image_left, y_image_bottom, "Аварийное освещение (Имеется): {}".format(
                    'Имеется' if subbuilding.emergency_lighting else 'Не Имеется'))
                p.drawString(x_image_right, y_image_bottom, "Дата изменения функционального назначения: {}".format(
                    subbuilding.change_functional_purpose_date.strftime('%d.%m.%Y')))
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom)
                y_image_bottom -= 6 * mm

                # Материал наружных стен
                y_image_bottom = self.draw_field_with_label(
                    p,
                    "Материал наружных стен:",
                    subbuilding.external_walls_material,
                    "Материал наружных стен:",
                    x_image_left,
                    y_image_bottom,
                    available_width=200 * mm,
                )
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom)

                # Класс функциональной ПО
                y_image_bottom = self.draw_labeled_text(
                    p,
                    "Класс функциональной ПО:",
                    subbuilding.functional_po_class,
                    x_image_left,
                    y_image_bottom,
                    available_width=200 * mm,
                    font_size=8,
                )
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom)
                # Степень огнестойкости
                y_image_bottom = self.draw_labeled_text(
                    p,
                    "Степень огнестойкости:",
                    subbuilding.fire_resistance_rating,
                    x_image_left,
                    y_image_bottom,
                    available_width=200 * mm,
                    font_size=8,
                )
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom)
                # Классификация лестницы
                y_image_bottom = self.draw_labeled_text(
                    p,
                    "Классификация лестницы:",
                    subbuilding.stairs_classification.all()[0],
                    x_image_left,
                    y_image_bottom,
                    available_width=200 * mm,
                    font_size=8,
                )
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom, font_size=9)
                # End of SubBuilding
                p.line(x_image_left, y_image_bottom, x_image_right_old * 2, y_image_bottom)
                y_image_bottom = self.check_and_create_new_page(p, y_image_bottom, font_size=9)

        # Add seal and signature section
        seal_x = 170 * mm  # Horizontal position
        seal_y = 30 * mm  # Vertical position from bottom
        self.add_seal_to_pdf(p, seal_x, seal_y, size=100)

        # Add signature line
        p.setFont(self.font_name, 10)
        p.line(20 * mm, 50 * mm, 100 * mm, 50 * mm)
        p.drawString(20 * mm, 45 * mm, f"Подпись ответственного лица: {self.building.owner.first_name} {self.building.owner.last_name}"
                                       f" {self.building.owner.middle_name}")

        # Add date
        current_date = datetime.now().strftime("%d.%m.%Y")
        p.drawString(20 * mm, 35 * mm, f"Дата: {current_date}")

        # Save PDF
        p.showPage()
        p.save()

        # Get the value of the BytesIO buffer
        pdf_file = buffer.getvalue()
        buffer.close()

        # Create filename
        filename = f'building_{self.building.id}_passport_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'

        # Save to BuildingPDFDocument model
        pdf_document = BuildingPDFDocument(building=self.building)
        pdf_document.file.save(filename, ContentFile(pdf_file), save=True)

        return pdf_document