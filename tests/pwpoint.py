from pptx import Presentation
import os

# Path to your company template
template_path = os.path.abspath("/home/dev/SlideAI/templates/company_template.pptx")

# Load the presentation
prs = Presentation(template_path)

# Print all available slide layout names and their indexes
print("Available slide layouts in company_template.pptx:\n")
for i, layout in enumerate(prs.slide_layouts):
    print(f"Index {i}: '{layout.name}'")
