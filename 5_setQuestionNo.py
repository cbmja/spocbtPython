import os
import re
from bs4 import BeautifulSoup

# div의 left 값 조건 목록
left_conditions = [
    "left:3.5381em;", "left:25.7261em;",
    "left:3.545em;", "left:25.75em;",
    "left:3.5361em;", "left:36.4502em;",
    "left:2.5981em;", "left:31.6373em;",
    "left:2.6em;", "left:31.66em;"
]

# 정규식을 사용하여 "숫자."로 시작하는 문자열 찾기
question_pattern = re.compile(r"^(\d+)\.")

def add_questionno_to_all_spans(input_dir, output_dir):
    """
    특정 left 속성을 가진 div 안의 모든 span 태그 중
    "숫자."로 시작하는 문자열에 data-questionno 속성을 추가
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # 출력 폴더 생성
    
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".html"):
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, file_name)
            
            # 파일 읽기
            with open(input_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
            
            # 조건에 맞는 div 태그 찾기
            for div in soup.find_all("div"):
                style = div.get("style", "")
                if any(cond in style for cond in left_conditions):
                    # div 안의 모든 span 태그 처리
                    for span in div.find_all("span"):
                        if span.string:
                            text = span.string.strip()
                            match = question_pattern.match(text)
                            if match:  # "숫자."로 시작하는 경우
                                span["data-questionno"] = match.group(1)  # 숫자만 추가
            
            # 수정된 파일 저장
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(str(soup))
            
            print(f"Processed: {file_name}")

# 경로 설정
input_dir = r"C:\Users\jeon\Desktop\온라인 자격증 시험\html변환 시연\6. 과목코드 data 부여 [ html ]"
output_dir = r"C:\Users\jeon\Desktop\온라인 자격증 시험\html변환 시연\7. 문제번호 data 부여 [ html ]"

add_questionno_to_all_spans(input_dir, output_dir)
