from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import PP_PLACEHOLDER
from pptx.dml.color import RGBColor
import os
from src.models.presentation import Presentation as PresentationModel


def generate_pptx_from_json(
    presentation: PresentationModel,
    template_path: str = "templates/base_template1.pptx",
    output_dir: str = "output"
) -> str:
    """
    Generates a PowerPoint file from a Presentation model using a given template.

    Args:
        presentation (PresentationModel): Pydantic model containing slides.
        template_path (str): Path to the .pptx template.
        output_dir (str): Directory where the generated .pptx will be saved.

    Returns:
        str: Path to the generated PowerPoint file.
    """
    prs = Presentation(template_path)

    # --- Title Slide ---
    title_slide_layout = prs.slide_layouts[0]  
    title_slide = prs.slides.add_slide(title_slide_layout)

    title_shape = title_slide.shapes.title
    subtitle_shape = title_slide.placeholders[1] if len(title_slide.placeholders) > 1 else None

    title_shape.text = presentation.title
    if subtitle_shape:
        subtitle_shape.text = "An AI-generated presentation"

    # --- Content Slides ---
    for slide_data in presentation.slides:
        slide_layout = prs.slide_layouts[1] 
        slide = prs.slides.add_slide(slide_layout)

        title_placeholder = None
        content_placeholder = None

        for shape in slide.placeholders:
            if shape.placeholder_format.type == PP_PLACEHOLDER.TITLE:
                title_placeholder = shape
            elif shape.placeholder_format.type in (PP_PLACEHOLDER.BODY, PP_PLACEHOLDER.OBJECT):
                content_placeholder = shape

        if not title_placeholder or not content_placeholder:
            raise ValueError("Template is missing a title or content placeholder.")

        title_placeholder.text = slide_data.heading

        bullet_points = slide_data.bullet_points or []
        key_message = slide_data.key_message

        content_placeholder.text = ""
        text_frame = content_placeholder.text_frame

        for i, bullet in enumerate(bullet_points):
            p = text_frame.add_paragraph() if i > 0 else text_frame.paragraphs[0]
            p.text = bullet
            p.level = 0
            p.font.size = Pt(18)

        if key_message:
            text_frame.add_paragraph()  
            p = text_frame.add_paragraph()
            p.text = key_message
            p.level = 0
            p.font.size = Pt(18)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 105, 180) 

    first_slide = prs.slides[0]
    if not first_slide.shapes.title or first_slide.shapes.title.text.strip() == "":
        xml_slides = prs.slides._sldIdLst
        slides = list(xml_slides)
        xml_slides.remove(slides[0])
    
    # --- Save ---
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
        print(f"[INFO] Created folder: {output_dir}")
    else:
        print(f"[INFO] Output folder already exists: {output_dir}")
    output_path = os.path.join(output_dir, f"{presentation.title.replace(' ', '_')}.pptx")
    prs.save(output_path)
    return output_path
