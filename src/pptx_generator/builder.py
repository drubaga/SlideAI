from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.enum.shapes import PP_PLACEHOLDER
from pptx.dml.color import RGBColor
import os
import requests
from serpapi import GoogleSearch

from src.models.presentation import Presentation as PresentationModel

class PPTXBuilder:
    def __init__(self, presentation: PresentationModel, template_path: str = "templates/base_template1.pptx", output_dir: str = "output", image_dir: str = "images"):
        self.presentation_model = presentation
        self.template_path = template_path
        self.output_dir = output_dir
        self.image_dir = image_dir
        self.prs = Presentation(template_path)

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

            # Insert image if keywords provided
          #  if hasattr(slide_data, "image_keywords") and slide_data.image_keywords:
            #    image_path = self._download_image(slide_data.image_keywords)
            #    if image_path:
              #      slide.shapes.add_picture(image_path, Inches(5.5), Inches(1.5), width=Inches(4))

   # def _download_image(self, keywords: str) -> str:
        #if not os.path.exists(self.image_dir):
           # os.makedirs(self.image_dir)

       # try:
          #  query = " ".join(keywords) if isinstance(keywords, list) else keywords
           # print(f"[INFO] Searching SerpAPI for: {query}")

           # api_key = os.getenv("SERPAPI_API_KEY")
           # if not api_key:
              #  raise ValueError("SERPAPI_API_KEY not found in environment.")

           # search = GoogleSearch({
              #  "q": query,
              #  "tbm": "isch",               # image search mode
               # "num": 1,
               # "api_key": api_key
           # })

           # results = search.get_dict()
           # images = results.get("images_results", [])

            #if not images:
              #  print(f"[WARN] No images found for '{query}'")
               # return None

           # image_url = images[0]["original"]
           # filename_safe_query = re.sub(r"[^\w\-_. ]", "_", query)
            # file_path = os.path.join(self.image_dir, f"{filename_safe_query}.jpg")

           # response = requests.get(image_url, timeout=10)
          #  response.raise_for_status()

           # with open(file_path, "wb") as f:
              #  f.write(response.content)

           # print(f"[INFO] Image saved for '{query}' → {file_path}")
           # return file_path

       # except Exception as e:
          #  print(f"[ERROR] SerpAPI image fetch failed for '{keywords}': {e}")
          #  return None


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
        else:
            print(f"[INFO] Output folder already exists: {self.output_dir}")

        output_path = os.path.join(self.output_dir, f"{self.presentation_model.title.replace(' ', '_')}.pptx")
        self.prs.save(output_path)
        return output_path
