from qdrant_client import QdrantClient, models
from typing import Optional
from uuid import uuid4

client = QdrantClient(
    url="http://localhost:6333"
)

COLLECTION_NAME = "business-docs"

class QdrantStore:
    def __init__(self,
                 url: str = "http://localhost:6333",
                 collection_name: str = COLLECTION_NAME,
                 vector_size: int = 1536):
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
        self.vector_size = vector_size

    def create_collection(self):
        if not self.client.collection_exists(collection_name=self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size,
                    distance=models.Distance.COSINE
                )
            )

    def upsert_documents(self, 
                         texts: list[str],
                         vectors: list[list[float]],
                         metadata: Optional[list[dict]] = None,
                         point_ids: Optional[list[str]] = None,
                         ):
        if len(texts) != len(vectors):
            raise ValueError("The length of texts and vectors must be the same.")
        if metadata is None:
            metadata = [{} for _ in texts]
        if metadata and len(metadata) != len(texts):
            raise ValueError("The length of metadata must match the length of texts.")

        if point_ids is None:
            point_ids =  [str(uuid4()) for i in range(len(texts))]

        if len(point_ids) != len(texts):
            raise ValueError("The length of point_ids must match the length of texts.")

        points = []
        for text, vector, metadata_item, point_id in zip(texts, vectors, metadata, point_ids):
            payload = {
                "text": text,
                **metadata_item
            }

            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=True
        )

        return point_ids

   
