import openai
from executor import executor
from extractor import extractor
from planner import planner
from summarizer import summarize
from executor import instructor
def main():
    # Yêu cầu người dùng nhập IP mục tiêu
    target_ip = input("Nhập IP mục tiêu để bắt đầu pentest: ")
    
    # API key cho OpenAI
    api_key = "YOUR_OPENAI_API_KEY"  # Đảm bảo thay thế bằng API key của bạn
    
    # Khởi tạo các module cần thiết
    planner = planner(target_ip, api_key)
    executor = executor(api_key)
    instructor = instructor(api_key, knowledge_base_path="path/to/knowledge_base.json")  # Đảm bảo cung cấp đúng đường dẫn
    summarizer = summarizer(api_key)
    extractor = extractor(api_key)

    # Thiết lập các module phụ trợ
    planner.executor = executor
    planner.summarizer = summarizer
    
    # Bắt đầu chạy pentest
    print("Đang chạy pentest...")
    planner.run()
    
    # Tạo lịch sử tấn công từ các nhiệm vụ đã hoàn thành
    attack_history = "\n".join(
        [f"Task: {task['task']}, Result: {task['description']}, Status: {task['status']}" 
         for task in planner.completed_tasks]
    )

    # Sử dụng Extractor để trích xuất thông tin lỗ hổng
    vulnerabilities = extractor.extract_vulnerabilities(attack_history)

    # Hiển thị kết quả cuối cùng
    print("\nKết quả trích xuất các lỗ hổng đã khai thác:")
    for vulnerability in vulnerabilities:
        print(f"Exploited: {vulnerability['exploited']}")
        print(f"Description: {vulnerability['description']}")
        print(f"Impact: {vulnerability['impact']}")
        print(f"Remediation: {vulnerability['remediation']}")
        print("-" * 40)

if __name__ == "__main__":
    main()
