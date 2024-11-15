import openai
import json
from executor.executor import Executor
from summarizer.summarize import Summarizer
class Planner:
    def __init__(self, target_ip: str, api_key: str):
        self.target_ip = target_ip
        self.api_key = api_key
        self.attack_plan = []
        self.completed_tasks = []
        self.executor = Executor(self.api_key)
        self.summarizer = Summarizer(self.api_key)
        self.exploited_vulnerabilities = []  # Danh sách lỗ hổng đã khai thác

    def generate_initial_tasks(self):
        """Khởi tạo các nhiệm vụ ban đầu khi có IP mục tiêu mới."""
        initial_tasks = [
            {"task": "Reconnaissance", "description": "Gather basic information about the target system.", "status": "to-do"},
            {"task": "Scanning", "description": f"Scan open ports and services on IP {self.target_ip}.", "status": "to-do"},
            {"task": "Vulnerability Assessment", "description": "Analyze scan results to identify vulnerabilities.", "status": "to-do"},
            {"task": "Exploitation", "description": "Attempt to exploit identified vulnerabilities.", "status": "to-do"}
        ]
        self.attack_plan.extend(initial_tasks)

    def run(self):
        # Nếu chưa có nhiệm vụ, tạo các nhiệm vụ ban đầu
        if not self.attack_plan:
            self.generate_initial_tasks()

        while self.attack_plan:
            current_task = self.attack_plan.pop(0)
            if current_task["status"] == "to-do":
                # Thực hiện nhiệm vụ
                # Thực hiện nhiệm vụ
                task_result = self.executor.run_task(current_task["description"])

                
                # Rút gọn kết quả
                summarized_result = self.summarizer.summarize(current_task, task_result)
                
                # Kiểm tra xem nhiệm vụ có thành công không
                if "success" in summarized_result["result"].lower():
                    # Cập nhật danh sách lỗ hổng đã khai thác
                    self.exploited_vulnerabilities.append(current_task)
                    # Gọi Counterfactual Prompting để giả định rằng lỗ hổng này không tồn tại
                    self._counterfactual_prompting()
                
                # Cập nhật trạng thái nhiệm vụ và sinh nhiệm vụ tiếp theo
                self._update_task_status(summarized_result)
                new_tasks = self._generate_next_tasks(summarized_result)
                self.attack_plan.extend(new_tasks)

    def _counterfactual_prompting(self):
        """Sử dụng Counterfactual Prompting để điều chỉnh kế hoạch tấn công."""
        if self.exploited_vulnerabilities:
            vulnerabilities = "\n".join([f"{v['task']}: {v['description']}" for v in self.exploited_vulnerabilities])
            counterfactual_prompt = (
                f"Here is the list of vulnerabilities already identified and exploited:\n{vulnerabilities}\n\n"
                "Now, please update the attack plan assuming these vulnerabilities do not exist, "
                "and consider alternative attack vectors to explore new potential vulnerabilities."
            )
            # Gửi prompt cho API ChatGPT để tạo task mới loại bỏ các lỗ hổng đã biết
            response = self._generate_attack_plan(counterfactual_prompt)
            self.attack_plan.extend(response)

    def _generate_attack_plan(self, prompt: str):
        openai.api_key=self.api_key
        """Gửi prompt đến API GPT để lấy danh sách các nhiệm vụ tiếp theo."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )
        new_tasks = response.choices[0].message['content']
        return [{"task": task.split(":")[0].strip(), "description": task.split(":")[1].strip(), "status": "to-do"} for task in new_tasks.splitlines() if ":" in task]

    def _update_task_status(self, summarized_result):
        """Cập nhật trạng thái nhiệm vụ hiện tại dựa trên kết quả."""
        status = "completed" if "success" in summarized_result["result"].lower() else "failed"
        summarized_result["status"] = status
        self.completed_tasks.append(summarized_result)

    def _generate_next_tasks(self, summarized_result):
        """Sinh nhiệm vụ tiếp theo dựa trên kết quả hiện tại."""
        if summarized_result["status"] == "completed":
            next_tasks = [
                {"task": "Further Scanning", "description": "Perform deeper scans to identify hidden services.", "status": "to-do"},
                {"task": "Privilege Escalation", "description": "Attempt privilege escalation based on new vulnerabilities.", "status": "to-do"}
            ]
            return next_tasks
        return []
    def save_results_to_json(self, filename="attack_data.json"):
        """Lưu trạng thái của kế hoạch tấn công và các lỗ hổng đã khai thác vào file JSON."""
        results = {
            "target_ip": self.target_ip,
            "attack_plan": self.attack_plan,
            "completed_tasks": self.completed_tasks,
            "exploited_vulnerabilities": self.exploited_vulnerabirunlities
        }
        with open(filename, "w") as f:
            json.dump(results, f, indent=4)
