import os
from bs4 import BeautifulSoup

def process_html_files(input_dir, output_dir):
    """
    span 태그에서 ①,②,③,④를 검색하여
    - 하나만 포함된 경우: data-answerno="1", "2", "3", "4" 추가
    - 둘 이상 포함된 경우: data-answerno="duplicate" 추가
    처리 후 통계를 TXT 파일로 저장
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # 출력 폴더 생성

    answer_numbers = {'①': '1', '②': '2', '③': '3', '④': '4'}
    summary_lines = []

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".html"):
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, file_name)

            with open(input_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")

            # 카운트 초기화
            total_count = 0
            count_1 = 0
            count_2 = 0
            count_3 = 0
            count_4 = 0
            count_duplicate = 0

            for span in soup.find_all("span"):
                if span.string:
                    text = span.string
                    matches = [answer_numbers[char] for char in text if char in answer_numbers]

                    if len(matches) == 1:
                        span["data-answerno"] = matches[0]
                        if matches[0] == '1':
                            count_1 += 1
                        elif matches[0] == '2':
                            count_2 += 1
                        elif matches[0] == '3':
                            count_3 += 1
                        elif matches[0] == '4':
                            count_4 += 1
                    elif len(matches) > 1:
                        span["data-answerno"] = "duplicate"
                        count_duplicate += 1

            total_count = count_1 + count_2 + count_3 + count_4 + count_duplicate

            # HTML 파일 저장
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(str(soup))

            # 결과를 summary_lines에 추가
            summary_line = (f"{file_name} / totalCnt: {total_count} / 1cnt: {count_1} / 2cnt: {count_2} "
                            f"/ 3cnt: {count_3} / 4cnt: {count_4} / duplicateCnt: {count_duplicate}")
            summary_lines.append(summary_line)

            print(f"Processed: {file_name}")

    # TXT 파일 생성
    summary_path = os.path.join(output_dir, "summary.txt")
    with open(summary_path, "w", encoding="utf-8") as summary_file:
        summary_file.write("\n".join(summary_lines))

    print(f"Summary file created at: {summary_path}")

# 경로 설정
input_dir = r"C:\\Users\\jeon\\Desktop\\온라인 자격증 시험\\html변환\\4. hidden 제거 [ html ]"
output_dir = r"C:\\Users\\jeon\\Desktop\\온라인 자격증 시험\\html변환\\sample"

process_html_files(input_dir, output_dir)
