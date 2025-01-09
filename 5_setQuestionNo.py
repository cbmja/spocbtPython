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
    "숫자."로 시작하는 문자열에 data-questionno 속성을 추가.
    data-subjectcode 속성의 개수(subjectcodeCnt)를 추가하여 요약.
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

            question_counts = {}
            total_question_count = 0
            total_subjectcode_count = len(soup.find_all(attrs={"data-subjectcode": True}))

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
                                question_no = match.group(1)
                                span["data-questionno"] = question_no  # 숫자만 추가
                                question_counts[question_no] = question_counts.get(question_no, 0) + 1
                                total_question_count += 1

            # 수정된 파일 저장
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(str(soup))

            # 통계 생성 (data-subjectcode 개수를 기준으로 필터링)
            filtered_summary = [
                f'data-questionno="{k}": {v}'
                for k, v in question_counts.items()
                if v != total_subjectcode_count  # data-subjectcode 개수와 다르면 포함
            ]
            summary_line = (
                f"{file_name}\n"
                f"subjectcodeCnt: {total_subjectcode_count}\n"
                f"totalCnt: {total_question_count}\n" +
                "\n".join(filtered_summary)
            )
            summary_lines.append(summary_line)

            print(f"Processed: {file_name}")

    # 요약 정보 저장
    summary_path = os.path.join(output_dir, "summary.txt")
    with open(summary_path, "w", encoding="utf-8") as summary_file:
        summary_file.write("\n\n".join(summary_lines))

    print(f"Summary file created at: {summary_path}")

# 경로 설정
input_dir = r"C:\Users\jeon\Desktop\온라인 자격증 시험\html변환\6. 과목코드 data 부여 [ html ]"
output_dir = r"C:\Users\jeon\Desktop\온라인 자격증 시험\html변환\7. 문제번호 data 부여 [ html ]"

add_questionno_to_all_spans(input_dir, output_dir)
