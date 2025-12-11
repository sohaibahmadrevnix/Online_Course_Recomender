from ddgs import DDGS
from app.src.rag_pipeline.llm_extract import extract_courses_from_text

async def internet_course_search(query: str):

    with DDGS() as ddg:
        results = ddg.text(
            f"{query} online course udemy coursera edx free tutorial",
            max_results=20
        )

    bodies = [r.get("body", "") for r in results]
    text = "\n".join(bodies)

    # Very important → require enough text
    if len(text) < 200:
        return []

    extracted = await extract_courses_from_text(text)
    
    return extracted[:5] if len(extracted) >= 5 else extracted
