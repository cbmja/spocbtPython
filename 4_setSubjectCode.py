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
    "운 동 역 학 (": "EB",
    "스포츠윤리 (": "SETH",
    "장애인스포츠론 (": "APS",
    "운동부하검사 (": "ELT",
    "운동처방론 (": "EPD",
    "기능해부학 (": "FA",
    "건강교육론 (": "HE",
    #"건강·체력평가 (": "HTA",
    "체력평가 (": "HTA",
    "운동상해 (": "IE",
    "운 동 상 해 (": "IE",
    "병태생리학 (": "PA",
    "유아체육론 (": "PAE",
    "체육측정평가론 (": "PME",
    "스포츠영양학 (": "SN",
    "노인체육론 (": "SPA",
    "특수체육론 (": "SPE",
    "트레이닝론 (": "TRN"
}

def add_subject_code_to_span(input_dir, output_dir):
    """
    HTML 파일의 <span> 태그에서 과목명을 검색하여
    data-subjectcode 속성을 추가하고, 중복되는 값 중 먼저 나오는 태그의
    data-subjectcode 속성만 삭제. 통계에서도 반영.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # 출력 폴더 생성

    summary_lines = []

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".html"):
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, file_name)

            # 파일 읽기
            with open(input_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")

            subject_counts = {}
            total_count = 0
            seen_subjectcodes = {}  # 중복 검사용 딕셔너리 {값: 해당 span}

            # <span> 태그만 처리
            for span in soup.find_all("span"):
                if span.string:  # 텍스트가 있는 경우
                    for key, value in subject_map.items():
                        if key in span.string:
                            # 중복 확인
                            if value in seen_subjectcodes:
                                # 이미 존재하는 경우, 이전 항목의 data-subjectcode 속성 제거
                                del seen_subjectcodes[value]["data-subjectcode"]
                                print(f"Removed data-subjectcode from: {seen_subjectcodes[value].string}")
                                # 통계에서 -1
                                subject_counts[value] -= 1
                                total_count -= 1
                            # 새 항목 추가
                            span["data-subjectcode"] = value
                            seen_subjectcodes[value] = span  # 최신 항목 저장
                            subject_counts[value] = subject_counts.get(value, 0) + 1
                            total_count += 1

            # 수정된 파일 저장
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(str(soup))

            # 통계 생성
            subject_summary = " / ".join([f"{k}: {v}" for k, v in subject_counts.items()])
            summary_line = f"{file_name} / totalCnt: {total_count} / {subject_summary}"
            summary_lines.append(summary_line)

            print(f"Processed: {file_name}")

    # TXT 파일 생성
    summary_path = os.path.join(output_dir, "summary.txt")
    with open(summary_path, "w", encoding="utf-8") as summary_file:
        summary_file.write("\n".join(summary_lines))

    print(f"Summary file created at: {summary_path}")

# 경로 설정
input_dir = r"C:\\Users\\jeon\\Desktop\\온라인 자격증 시험\\html변환\\5. 보기 번호 data 부여 [ html ]"
output_dir = r"C:\\Users\\jeon\\Desktop\\온라인 자격증 시험\\html변환\\6. 과목코드 data 부여 [ html ]"

add_subject_code_to_span(input_dir, output_dir)
