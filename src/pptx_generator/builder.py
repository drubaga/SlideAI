from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.enum.shapes import PP_PLACEHOLDER, MSO_SHAPE
from pptx.dml.color import RGBColor
import os

from src.models.presentation import Presentation as PresentationModel

# Delay image fetcher imports to runtime based on user input
class PPTXBuilder:
    def __init__(
        self,
        presentation: PresentationModel,
        template_path: str = "templates/base_template1.pptx",
        output_dir: str = "output",
        image_dir: str = "images",
        enable_images: bool = False,
        image_provider: str = None
    ):
        self.presentation_model = presentation
        self.template_path = template_path
        self.output_dir = output_dir
        self.image_dir = image_dir
        self.enable_images = enable_images
        self.image_provider = image_provider
        self.prs = Presentation(template_path)

        # Dynamically assign image fetcher
        self.image_fetcher = None
        if self.enable_images and self.image_provider:
            if self.image_provider == "pexels":
                from src.image_generators.pexels_image_generator import PexelsImageGenerator
                self.image_fetcher = PexelsImageGenerator(self.image_dir)
            elif self.image_provider == "serpapi":
                from src.image_generators.serpapi_image_generator import SerpApiImageGenerator
                self.image_fetcher = SerpApiImageGenerator(self.image_dir)

    def build(self) -> str:
        self._add_title_slide()
        self._add_content_slides()
        self._remove_blank_first_slide()
        return self._save_presentation()

    def _add_title_slide(self):
        layout = self.prs.slide_layouts[0]
        slide = self.prs.slides.add_slide(layout)
        title = slide.shapes.title
        subtitle = slide.placeholders[1] if len(slide.placeholders) > 1 else None
        title.text = self.presentation_model.title
        if subtitle:
            subtitle.text = "An AI-generated presentation"

    def _add_content_slides(self):
        layout = self.prs.slide_layouts[1]
        for slide_data in self.presentation_model.slides:
            slide = self.prs.slides.add_slide(layout)
            title_ph, content_ph = self._find_placeholders(slide)

            if not title_ph or not content_ph:
                raise ValueError("Template is missing a title or content placeholder.")

            title_ph.text = slide_data.heading
            text_frame = content_ph.text_frame
            text_frame.clear()

            for i, bullet in enumerate(slide_data.bullet_points or []):
                p = text_frame.add_paragraph() if i > 0 else text_frame.paragraphs[0]
                p.text = bullet
                p.level = 0
                p.font.size = Pt(18)

            if slide_data.key_message:
                p = text_frame.add_paragraph()
                p.text = slide_data.key_message
                p.level = 0
                p.font.size = Pt(18)
                p.font.bold = True
                p.font.color.rgb = RGBColor(255, 105, 180)

            # Insert image
            if self.image_fetcher and slide_data.image_keywords:
                keywords = slide_data.image_keywords
                if isinstance(keywords, list):
                    keywords = " ".join(keywords)
                image_path = self.image_fetcher.fetch_image(keywords)
                if image_path:
                    self._insert_image_with_border(slide, image_path)

    def _insert_image_with_border(self, slide, image_path):
        margin = Inches(0.3)
        image_width = Inches(4.0)
        image_height = Inches(3.0)
        border_thickness = Pt(2)

        slide_width = self.prs.slide_width
        slide_height = self.prs.slide_height

        left = slide_width - image_width - margin
        top = slide_height - image_height - margin

        # Insert border first (behind)
        border = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            left - Pt(2),
            top - Pt(2),
            image_width + Pt(4),
            image_height + Pt(4)
        )
        slide.shapes._spTree.remove(border._element)
        slide.shapes._spTree.insert(2, border._element)
        border.fill.background()
        border.line.width = border_thickness
        border.line.color.rgb = RGBColor(0, 0, 0)

        # Insert image on top
        slide.shapes.add_picture(image_path, left, top, width=image_width, height=image_height)

    def _find_placeholders(self, slide):
        title_ph = None
        content_ph = None
        for shape in slide.placeholders:
            if shape.placeholder_format.type == PP_PLACEHOLDER.TITLE:
                title_ph = shape
            elif shape.placeholder_format.type in (PP_PLACEHOLDER.BODY, PP_PLACEHOLDER.OBJECT):
                content_ph = shape
        return title_ph, content_ph

    def _remove_blank_first_slide(self):
        first = self.prs.slides[0]
        if not first.shapes.title or first.shapes.title.text.strip() == "":
            xml_slides = self.prs.slides._sldIdLst
            xml_slides.remove(list(xml_slides)[0])

    def _save_presentation(self) -> str:
        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"[INFO] Created folder: {self.output_dir}")
        output_path = os.path.join(self.output_dir, f"{self.presentation_model.title.replace(' ', '_')}.pptx")
        self.prs.save(output_path)
        return output_path
