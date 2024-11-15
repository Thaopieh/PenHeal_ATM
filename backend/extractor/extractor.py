import openai

class Extractor:
    def __init__(self, api_key):
        self.api_key = api_key

    def extract_vulnerabilities(self, attack_history):
        """
        Trích xuất thông tin về các lỗ hổng từ lịch sử tấn công.
        
        Parameters:
            attack_history (str): Lịch sử tấn công dạng văn bản.

        Returns:
            list: Danh sách các lỗ hổng đã khai thác với thông tin chi tiết.
        """
        # Tạo prompt để trích xuất lỗ hổng
        prompt = (
            "You are a vulnerability extractor for penetration testing results. "
            "Given the following attack history, extract information about each vulnerability in the format:\n\n"
            "Exploited: [backdoor/CVE ID]\n"
            "Description: [Brief description of the vulnerability]\n"
            "Impact: [Potential impact of the vulnerability]\n"
            "Remediation: [Suggested remediation steps]\n\n"
            "For vulnerabilities without a disclosed CVE, use 'CVE-NA' instead of an ID.\n\n"
            f"Attack History:\n{attack_history}\n\n"
            "Please provide the extracted vulnerability information in the specified format."
        )

        # Gọi API của OpenAI để trích xuất thông tin
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an extractor for penetration testing outputs."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200  # Giới hạn số lượng token cho mỗi lần trả lời để có định dạng cố định
        )

        # Lấy thông tin về các lỗ hổng đã khai thác từ API
        extracted_info = response.choices[0].message["content"].strip()

        # Chuyển đổi thông tin trích xuất thành danh sách các lỗ hổng
        vulnerabilities = self._parse_extracted_info(extracted_info)
        
        return vulnerabilities

    def _parse_extracted_info(self, extracted_info):
        """
        Phân tích thông tin trích xuất để tạo danh sách các lỗ hổng dạng dictionary.
        
        Parameters:
            extracted_info (str): Thông tin trích xuất dưới dạng văn bản.

        Returns:
            list: Danh sách các lỗ hổng với các thuộc tính (exploited, description, impact, remediation).
        """
        vulnerabilities = []
        blocks = extracted_info.split("Exploited: ")  # Chia từng lỗ hổng
        for block in blocks[1:]:  # Bỏ qua phần đầu nếu nó không chứa lỗ hổng
            lines = block.strip().splitlines()
            vulnerability = {
                "exploited": lines[0].strip() if lines else "CVE-NA",
                "description": "",
                "impact": "",
                "remediation": ""
            }
            for line in lines[1:]:  # Bắt đầu từ dòng thứ 2 trở đi để lấy thông tin chi tiết
                if line.startswith("Description:"):
                    vulnerability["description"] = line.split("Description:", 1)[1].strip()
                elif line.startswith("Impact:"):
                    vulnerability["impact"] = line.split("Impact:", 1)[1].strip()
                elif line.startswith("Remediation:"):
                    vulnerability["remediation"] = line.split("Remediation:", 1)[1].strip()
            vulnerabilities.append(vulnerability)
        
        return vulnerabilities
