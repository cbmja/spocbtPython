import fitz  # PyMuPDF
import json
import os

# JSON 저장 경로
json_output_path = r"C:\Users\jeon\Desktop\border\res_json.json"

# 폴더가 없으면 생성
os.makedirs(os.path.dirname(json_output_path), exist_ok=True)

# 테두리 좌표 저장을 위한 리스트
border_data = []

# PDF 열기
pdf_path = r"c:\Users\jeon\Desktop\시험_사이트\수능 기출 모음\2025\2025_국어영역_문제지_짝수형.pdf"
doc = fitz.open(pdf_path)

# 5 포인트 패딩 적용
padding = 5

# 모든 페이지에 대해 작업
for page_num in range(doc.page_count):
    page = doc.load_page(page_num)

    # 겹치는 테두리를 병합할 사각형 리스트
    rects = []

    for block in page.get_text("dict")["blocks"]:
        if "lines" in block:  # 텍스트 블록인 경우
            # 패딩을 적용하여 사각형 계산
            rect = fitz.Rect(
                block["bbox"][0] - padding,  # 왼쪽
                block["bbox"][1] - padding,  # 위쪽
                block["bbox"][2] + padding,  # 오른쪽
                block["bbox"][3] + padding   # 아래쪽
            )
            rects.append(rect)

    # 겹치는 사각형 병합
    merged_rects = []
    while rects:
        rect = rects.pop(0)
        # 병합된 사각형에 포함될지 확인
        merged = False
        for idx, merged_rect in enumerate(merged_rects):
            if merged_rect.intersects(rect):  # 겹칠 경우 병합
                merged_rects[idx] = merged_rect | rect  # 사각형 병합
                merged = True
                break
        if not merged:
            merged_rects.append(rect)  # 겹치지 않으면 새로운 사각형 추가

    # 병합된 사각형 정보 저장
    for merged_rect in merged_rects:
        border_data.append({
            "page": page_num + 1,
            "x": merged_rect.x0,
            "y": merged_rect.y0,
            "width": merged_rect.width,
            "height": merged_rect.height
        })

# JSON 파일로 저장
try:
    with open(json_output_path, "w", encoding="utf-8") as json_file:
        json.dump(border_data, json_file, indent=4)
    print(f"JSON 파일이 성공적으로 저장되었습니다: {json_output_path}")
except Exception as e:
    print(f"JSON 저장 중 오류 발생: {e}")
