import openai
import os
import json
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

class Planner:
    def __init__(self, model_name="gpt-3.5-turbo-1106"):
        openai.api_key = os.getenv("GPT_API_KEY")  # Lấy API key từ biến môi trường

        # Load thông tin model từ file JSON
        with open("models.json", "r") as file:
            self.models = json.load(file)

        # Kiểm tra xem model có tồn tại không
        if model_name not in self.models["openai"]:
            raise ValueError(f"Model {model_name} not found in models.json")
        
        # Lấy thông tin model
        self.model_info = self.models["openai"][model_name]
        self.model_name = model_name

    def create_plan(self, ip_address):
        # Prompt mẫu cố định cho việc tạo kế hoạch pentesting
        prompt = (
            f"You are a pentesting expert. Generate a detailed pentesting plan for the target IP address: {ip_address}. "
            "Include steps for reconnaissance, scanning, exploitation, and reporting vulnerabilities, with "
            "considerations for network and application layer security."
        )

        # Gọi API của OpenAI để tạo kế hoạch pentesting
        response = openai.Completion.create(
            engine=self.model_name,
            prompt=prompt,
            max_tokens=500
        )

        # Trả về kế hoạch từ phản hồi của API
        plan = response.choices[0].text.strip()
        return plan

    def get_model_info(self):
        # Trả về thông tin chi tiết về model
        return self.model_info
