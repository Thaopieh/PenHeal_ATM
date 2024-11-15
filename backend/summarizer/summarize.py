import openai

class Summarizer:
    def __init__(self, api_key):
        self.api_key = api_key

    def summarize(self, task, task_result):
        """
        Tóm tắt đầu ra từ Executor cho nhiệm vụ được giao.
        
        Parameters:
            task (dict): Thông tin về nhiệm vụ (bao gồm mô tả).
            task_result (dict): Kết quả từ Executor, bao gồm trạng thái và đầu ra.

        Returns:
            dict: Bản tóm tắt của kết quả nhiệm vụ.
        """
        # Tạo prompt để tóm tắt kết quả
        prompt = (
            f"The following is the result of a penetration testing task.\n\n"
            f"Task: {task['task']}\n"
            f"Description: {task['description']}\n"
            f"Result: {task_result['output']}\n\n"
            "Please provide a concise summary of this result. "
            "Focus on key findings, vulnerabilities, and any relevant details that could aid in decision-making."
        )
        openai.api_key=self.api_key
        # Gọi API của OpenAI để tạo tóm tắt
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a summarizer for penetration testing outputs."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100  # Giới hạn số lượng token để tránh tóm tắt quá dài
        )

        # Lấy bản tóm tắt từ API
        summary = response.choices[0].message["content"].strip()

        # Tạo kết quả cuối cùng
        summarized_result = {
            "task": task["task"],
            "description": task["description"],
            "summary": summary,
            "result": task_result["status"]  # Bao gồm trạng thái của task (success, failed)
        }

        return summarized_result
