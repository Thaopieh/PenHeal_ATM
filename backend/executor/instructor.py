import openai
import faiss
import json
import numpy as np

class Instructor:
    def __init__(self, api_key, knowledge_base_path):
        self.api_key = api_key
        self.knowledge_base = self.load_knowledge_base(knowledge_base_path)
        self.index = self.build_faiss_index()

    def load_knowledge_base(self, path):
        """Load knowledge base từ file JSON."""
        with open(path, "r") as f:
            return json.load(f)

    def build_faiss_index(self):
        """Xây dựng FAISS index từ knowledge base."""
        dimension = 1536  # Dimension của OpenAI embedding
        index = faiss.IndexFlatL2(dimension)
        self.vectors = []
        for entry in self.knowledge_base:
            vector = np.array(entry["vector"]).astype("float32")
            self.vectors.append(vector)
            index.add(vector.reshape(1, -1))
        return index

    def embed_task(self, task_description):
        """Tạo vector embedding cho nhiệm vụ."""
        response = openai.Embedding.create(
            input=task_description,
            model="text-embedding-ada-002"
        )
        return np.array(response["data"][0]["embedding"]).astype("float32")

    def retrieve_knowledge(self, task_description, top_k=3):
        """Truy xuất thông tin liên quan từ knowledge base."""
        task_vector = self.embed_task(task_description)
        distances, indices = self.index.search(task_vector.reshape(1, -1), top_k)
        retrieved = [self.knowledge_base[i] for i in indices[0]]
        return retrieved

    def generate_prompt(self, task_description):
        """Tạo prompt cho Executor dựa trên nhiệm vụ và kiến thức liên quan."""
        retrieved_info = self.retrieve_knowledge(task_description)
        excerpts = "\n".join(
            [f"{i+1}. {entry['info']}" for i, entry in enumerate(retrieved_info)]
        )
        prompt = (
            f"Here is a brief introduction to the task:\n{task_description}\n"
            f"Here is some info from the knowledge base for your reference:\n{excerpts}"
        )
        return prompt
