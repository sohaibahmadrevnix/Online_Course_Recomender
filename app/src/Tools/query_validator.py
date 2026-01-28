from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

class QueryValidator:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    async def validate_query(self, query: str) -> bool:
        """
        Analyzes a user's input to determine whether it is related to online courses, 
        learning, education, skill development, certifications, or course recommendations.
        Returns True if related, False otherwise.
        """
        system_prompt = """
        You are a query validation assistant. Your task is to determine if a user's input is related to:
        - Online courses
        - Learning or Education
        - Skill development
        - Certifications
        - Course recommendations

        Reply ONLY with 'VALID' if the query is related to any of these topics.
        Reply ONLY with 'INVALID' if the query is NOT related to these topics.
        Do not provide any explanation.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=0,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ]
            )
            
            result = response.choices[0].message.content.strip().upper()
            return result == "VALID"
        except Exception as e:
            print(f"Error in QueryValidator: {e}")
            # Fallback to True to avoid blocking legitimate queries if the LLM fails
            return True
