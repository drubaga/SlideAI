from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import PP_PLACEHOLDER
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

    for slide_data in presentation.slides:
        slide_layout = prs.slide_layouts[1]  # Title and Content layout
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

        # Clear any existing content
        content_placeholder.text = ""
        text_frame = content_placeholder.text_frame

        for i, bullet in enumerate(bullet_points):
            p = text_frame.add_paragraph() if i > 0 else text_frame.paragraphs[0]
            p.text = bullet
            p.level = 0

        if key_message:
            text_frame.add_paragraph()  # line break
            p = text_frame.add_paragraph()
            p.text = f"Key Message: {key_message}"
            p.level = 0

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{presentation.title.replace(' ', '_')}.pptx")
    prs.save(output_path)
    return output_path
