import subprocess
import openai

class Executor:
    def __init__(self, api_key):
        self.api_key = api_key

    def generate_command(self, task_description):
        """Tạo lệnh từ nhiệm vụ do Planner giao cho."""
        system_prompt = (
            "You are a command generator for penetration testing. Generate commands that are simple and "
            "formatted with '$' at the start and end. Avoid overly verbose commands. Example: "
            "$nmap --script vuln [target IP]$."
        )
        
        # Tạo prompt từ mô tả nhiệm vụ của Planner
        prompt = f"{system_prompt}\nTask: {task_description}"
        
        openai.api_key=self.api_key
        # Gọi API của ChatGPT để tạo lệnh
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50  # Giới hạn để tránh lệnh quá dài
        )

        # Kết quả từ API, lọc để lấy lệnh với định dạng $
        command = response.choices[0].message["content"].strip()
        if command.startswith("$") and command.endswith("$"):
            return command[1:-1].strip()  # Bỏ ký hiệu $ để thực thi trong subprocess
        else:
            raise ValueError("Command is not properly formatted with '$' symbols.")

    def execute_command(self, command):
        """Thực thi lệnh trong terminal và trả về kết quả."""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
            return {"status": "success" if result.returncode == 0 else "failed", "output": output}
        except Exception as e:
            return {"status": "error", "output": str(e)}

    def run_task(self, task_description):
        """Nhận mô tả nhiệm vụ, tạo và thực thi lệnh, trả về kết quả."""
        command = self.generate_command(task_description)
        print(f"Executing command: {command}")
        result = self.execute_command(command)
        return result
