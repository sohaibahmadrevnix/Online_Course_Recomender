from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from app.src.rag_pipeline.rag_agent import RagCourseAgent
from app.dep.dependencies import get_current_user, get_db
from app.db.models.query_model import UserQuery
from app.api.routes.schema import QueryRequest, QueryResponse, CourseItem
import json


router = APIRouter()
agent = RagCourseAgent()

@router.post("/query" , response_model=QueryResponse)
async def search_courses(req: QueryRequest , current_user = Depends(get_current_user),db: Session = Depends(get_db)):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    result = await agent.search(req.query)
    user_query = UserQuery(
    user_id=current_user.id,
    query_text=req.query,
    response_text=json.dumps(result)
    )
    db.add(user_query)
    db.commit()
    if result != {}:
        result_list = result.get("results", [])
        items = []
        for res in result_list:
            items.append(
                CourseItem(
                    subject=res.get("subject", ""),
                    level=res.get("level", ""),
                    reviews=int(res.get("num_reviews", 0)),
                    price=str(res.get("price", "Free")),
                    duration=str(res.get("duration", 0)),
                    url=res.get("url", "")
                )
            )

        return QueryResponse(items=items, query=req.query)
    else:
        raise HTTPException(status_code=400, detail="There is not any course related to this in the dataset and not found any in the internet.")

    # return result
