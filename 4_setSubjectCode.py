import os
from bs4 import BeautifulSoup

# 텍스트와 subject_code 매핑
subject_map = {
    "스포츠사회학 (": "SS",
    "스포츠교육학 (": "SE",
    "스포츠심리학 (": "SP",
    "한국체육사 (": "KHS",
    "운동생리학 (": "EP",
    "운동역학 (": "EB",
    "스포츠윤리 (": "SETH"
}

def add_subject_code_to_span(input_dir, output_dir):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # 출력 폴더 생성
    
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".html"):
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, file_name)
            
            # 파일 읽기
            with open(input_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
            
            # <span> 태그만 처리
            for span in soup.find_all("span"):
                if span.string:  # 텍스트가 있는 경우
                    for key, value in subject_map.items():
                        if key in span.string:
                            span["data-subjectcode"] = value
            
            # 수정된 파일 저장
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(str(soup))
            
            print(f"Processed: {file_name}")

# 경로 설정
input_dir = r"C:\Users\jeon\Desktop\온라인 자격증 시험\html변환 시연\5. 보기 번호 data 부여 [ html ]"
output_dir = r"C:\Users\jeon\Desktop\온라인 자격증 시험\html변환 시연\6. 과목코드 data 부여 [ html ]"

add_subject_code_to_span(input_dir, output_dir)
