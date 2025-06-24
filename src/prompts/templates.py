def build_prompt(txt_path: str, user_query: str) -> str:
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            context = f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {txt_path}")
    except Exception as e:
        raise Exception(f" Error reading file: {e}")

    prompt = f"""
You are a helpful and intelligent assistant experienced in creating full PowerPoint-style presentations.

Your task is to generate a complete presentation (around 10-12 slides) based on the content and user instructions below.

---

### Requirements:
- Begin with an **intro slide** that includes the date and topic title
- Create **content slides** with slide titles and clear, descriptive bullet points
- Include **short examples or case illustrations** on 2-3 slides (when relevant)
- Include **one step-by-step process slide**, using '>>' to indicate each step
- Add a **key takeaway slide** before the final slides
- End with a **conclusion** and a **thank you** slide

---

### Output Format (Valid JSON):

{{
  "title": "Presentation Title",
  "slides": [
    {{
      "heading": "Slide Title",
      "bullet_points": [
        "Bullet point 1",
        "Bullet point 2"
      ],
      "key_message": "Optional summary of this slide",
      "img_keywords": "keywords for visuals"
    }},
    ...
  ]
}}

---

### User Query:
{user_query}

---

### Source Text:
{context}

---

Make sure the output is valid JSON, well-structured, and follows the requested slide structure.
"""

    return prompt

