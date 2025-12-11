from groq import Groq
import json
import os 
from app.src.rag_pipeline.courses_schema import format_course_item
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

SYSTEM_PROMPT = """
Extract ONLY online courses and format them as a JSON list.
Each item MUST contain:
subject, level, reviews, price, duration, url
Return ONLY valid JSON, no explanation.
"""

async def extract_courses_from_text(text):
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ]
        )

        out = res.choices[0].message.content.strip()

        # Try strict JSON parse
        items = json.loads(out)

    except Exception:
        # if model outputs invalid JSON → try to fix it
        try:
            fixed = out[out.find("["): out.rfind("]")+1]
            items = json.loads(fixed)
        except Exception:
            return []  # final fallback → return empty list

    # format items
    return [format_course_item(i) for i in items]

