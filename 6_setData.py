import os
from bs4 import BeautifulSoup
import re

class ExampleSetting:
    
    def __infos__(self):
        self.subjectCode = ""  # 과목코드
        self.questionNo = ""  # 문제 번호 1,2, ~ 20
        self.optionNo = ""  # 문제의 보기 번호 1,2,3,4

    def run(self, htmlFile, outputFile):
        self.__infos__()
        self.current_file_name = os.path.basename(htmlFile)  # 현재 파일 이름 저장
        
        with open(htmlFile, 'r', encoding='utf-8') as file:
            self.soup = BeautifulSoup(file, 'html.parser')

            # 하나의 페이지
            pageDiv = self.soup.find_all('div', class_='stl_ stl_02')

            # 결과 출력
            for div in pageDiv:
                pageList = div.find_all()
                self.setDataAttribute(pageList)

        # 수정된 파일 저장
        self.saveHtml(outputFile)

    def setDataAttribute(self, pageList):
        # 왼쪽 오른쪽을 분리하고 하나로 이어 붙임
        divList = self.seperateLeftRight(pageList)

        # 분리된 문제에 대해 보기별 문제번호 시험과목등을 설정한다.
        for dlist in divList:
            for div in dlist:
                # 시험과목과 과목코드를 찾는다.
                self.findExamSubject(div)

                if div.has_attr('data-answerno') or div.find('span', {'data-answerno': True}):
                    target_tag = div if div.has_attr('data-answerno') else div.find('span', {'data-answerno': True})
                    print(f"Processing1")

                if div.has_attr('data-questionno') or div.find('span', {'data-questionno': True}):
                    number_tag = div if div.has_attr('data-questionno') else div.find('span', {'data-questionno': True})
                    number = number_tag['data-questionno']
                    print(f"Processing2")

                if div.has_attr('data-subjectcode') or div.find('span', {'data-subjectcode': True}):
                    scode_tag = div if div.has_attr('data-subjectcode') else div.find('span', {'data-subjectcode': True})
                    scode = scode_tag['data-subjectcode']
                    self.subjectCode = scode
                    print(f"Processing3")

                if div.has_attr('data-answerno') or div.find('span', {'data-answerno': True}):
                    target_tag = div if div.has_attr('data-answerno') else div.find('span', {'data-answerno': True})
                    target_tag['data-subjectcode'] = self.subjectCode  # self.subjectCode 속성 추가
                    target_tag['data-questionno'] = number
                    print(f"Processing4")
                    continue

    def seperateLeftRight(self, pageList):
        leftDivList = []
        rightDivList = []
        returnList = []

        # 현재 파일 이름을 기준으로 기준값 설정
        file_name = self.current_file_name
        if any(year in file_name for year in ['2016', '2017', '2018', '2019', '2020']):
            left_threshold = 25
        elif '2021' in file_name:
            left_threshold = 36
        elif any(year in file_name for year in ['2022', '2023']):
            left_threshold = 31
        else:
            left_threshold = 31  # 기본값

        for div in pageList:
            style_attr = div.get('style')
            if style_attr:
                left_value = re.search(r'left:\s*([\d.]+)em', style_attr)
                if left_value:
                    left_em = float(left_value.group(1))
                    if left_em < left_threshold:
                        leftDivList.append(div)
                    else:
                        rightDivList.append(div)

        returnList.append(leftDivList)
        returnList.append(rightDivList)
        return returnList

    def findExamSubject(self, div):
        # data-subjectcode 속성의 값을 찾음
        subj_code = div.get('data-subjectcode')
        if subj_code:
            self.subjectCode = subj_code

    def saveHtml(self, outputFile):
        # 변경된 HTML을 파일에 쓰기
        with open(outputFile, 'w', encoding='utf-8') as file:
            file.write(str(self.soup))

def process_html_files(input_dir, output_dir):
    """
    입력 디렉터리의 모든 HTML 파일을 변환하여 출력 디렉터리에 저장
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # 출력 폴더 생성

    example = ExampleSetting()

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.html'):
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, file_name)
            example.run(input_path, output_path)

# 경로 설정
input_dir = r"C:\Users\jeon\Desktop\온라인 자격증 시험\html변환 시연\7. 문제번호 data 부여 [ html ]"
output_dir = r"C:\Users\jeon\Desktop\온라인 자격증 시험\html변환 시연\8. 보기에 과목코드 , 문제번호 data 부여 [ html ]"

# 실행
process_html_files(input_dir, output_dir)
