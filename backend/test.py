import openai
from dotenv import load_dotenv
import os

# Tải các biến môi trường từ file .env nếu có
load_dotenv()

# Kiểm tra nếu API key đã được thiết lập
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    print("API key chưa được cung cấp!")
else:
    print("API key đã được thiết lập!")

# Cập nhật API key cho OpenAI
openai.api_key = api_key

# Gọi OpenAI API để kiểm tra kết nối
try:
    # Thực hiện một request đơn giản để kiểm tra
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Chào bạn!"},  # Test message
            {"role": "user", "content": "Xin chào!"}
        ]
    )
    print("Kết quả trả về từ OpenAI:")
    print(response)

except openai.error.AuthenticationError as e:
    print(f"Lỗi xác thực: {e}")
except Exception as e:
    print(f"Lỗi khi kết nối đến OpenAI: {e}")
