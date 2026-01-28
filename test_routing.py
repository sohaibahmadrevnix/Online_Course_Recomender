import asyncio
import os
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

from app.src.Tools.router import CourseRouter

async def test_routing():
    router = CourseRouter()
    
    test_queries = [
        "I want to learn Python for data science",
        "Best web development courses for beginners",
        "How to get a Java certification?",
        "What's the weather like in Tokyo?",
        "How to bake a chocolate cake?",
        "Tell me a joke"
    ]
    
    for query in test_queries:
        print(f"\n--- Testing Query: '{query}' ---")
        result = await router.route_and_execute(query)
        
        if isinstance(result, dict) and result.get("error") == "invalid_query":
            print(f"Outcome: INVALID (Correctly rejected)")
            print(f"Message: {result.get('message')}")
        else:
            print(f"Outcome: VALID (Correctly accepted)")
            print(f"Source: {result.get('source')}")
            print(f"Number of results: {len(result.get('results', []))}")

if __name__ == "__main__":
    asyncio.run(test_routing())
