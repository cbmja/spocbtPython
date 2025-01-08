import os
from bs4 import BeautifulSoup

def process_html_files(input_dir, output_dir):
    """
    span 태그에서 ①,②,③,④를 검색하여
    - 하나만 포함된 경우: data-answerno="1", "2", "3", "4" 추가
    - 둘 이상 포함된 경우: data-answerno="duplicate" 추가
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # 출력 폴더 생성
    
    answer_numbers = {'①': '1', '②': '2', '③': '3', '④': '4'}
    
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".html"):
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, file_name)
            
            with open(input_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
            
            for span in soup.find_all("span"):
                if span.string:
                    text = span.string
                    matches = [answer_numbers[char] for char in text if char in answer_numbers]
                    
                    if len(matches) == 1:
                        span["data-answerno"] = matches[0]
                    elif len(matches) > 1:
                        span["data-answerno"] = "duplicate"
            
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(str(soup))
            
            print(f"Processed: {file_name}")

# 경로 설정
input_dir = r"C:\Users\jeon\Desktop\온라인 자격증 시험\html변환 시연\4. hidden 제거 [ html ]"
output_dir = r"C:\Users\jeon\Desktop\온라인 자격증 시험\html변환 시연\5. 보기 번호 data 부여 [ html ]"

process_html_files(input_dir, output_dir)
