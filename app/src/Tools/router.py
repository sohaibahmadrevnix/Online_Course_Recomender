from app.src.Tools.query_validator import QueryValidator
from app.src.rag_pipeline.rag_agent import RagCourseAgent

class CourseRouter:
    def __init__(self):
        self.validator = QueryValidator()
        self.agent = RagCourseAgent()

    async def route_and_execute(self, query: str):
        """
        Routes the query based on validation results.
        If valid, forwards to RAG agent.
        If invalid, returns a direct response message.
        """
        is_valid = await self.validator.validate_query(query)
        
        if is_valid:
            return await self.agent.search(query)
        else:
            return {
                "error": "invalid_query",
                "message": "The query is invalid and should be related to online courses, learning, education, skill development, certifications, or course recommendations."
            }
