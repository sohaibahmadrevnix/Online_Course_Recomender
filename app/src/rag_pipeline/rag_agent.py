import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

from app.src.rag_pipeline.internet_search import internet_course_search
from app.src.rag_pipeline.courses_schema import format_course_item


class RagCourseAgent:
    def __init__(self, csv_path="app/src/rag_pipeline/data/courses_dataset.csv"):

        # load CSV dataset
        df = pd.read_csv(csv_path)

        self.dataset = df.to_dict(orient="records")

        # text for embedding (title + subject)
        self.texts = [
            f"{item.get('level', '')} {item.get('subject', '')}"
            for item in self.dataset
        ]

        # free embedding model
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        # embeddings
        self.embeddings = self.model.encode(self.texts)

        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)

    async def search(self, query: str):

        query_emb = self.model.encode([query])

        D, I = self.index.search(query_emb, k=5)

        # threshold check (lower distance = better)
        if D[0][0] < 0.85:
            local_results = [
                format_course_item(self.dataset[i]) for i in I[0]
            ]
            if "title" in local_results:
                del local_results["title"]
            return {
                "source": "dataset",
                "results": local_results
            }

        # fallback → internet search
        fetched = await internet_course_search(query)

        return {
            "source": "internet",
            "results": fetched
        }
