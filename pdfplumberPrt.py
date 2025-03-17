import pdfplumber

pdf_path = r"C:\Users\jeon\Desktop\시험_사이트\pdf_py_lib\2025_kor_odd.pdf"
output_path = r"C:\Users\jeon\Desktop\시험_사이트\pdf_py_lib\output.txt"

# PDF 열기 및 결과 저장
with pdfplumber.open(pdf_path) as pdf, open(output_path, "w", encoding="utf-8") as output_file:
    for i, page in enumerate(pdf.pages):
        output_file.write(f"\n---+++--- Page {i+1} ---+++---\n")

        # 1. 텍스트 추출
        text = page.extract_text()
        if text:
            output_file.write("Text:\n" + text + "\n")
        else:
            output_file.write("Text: (No text found)\n")

        # 2. 글꼴 및 폰트 크기 추출
        output_file.write("\n---+++--- Font Information ---+++---\n")
        for char in page.chars:
            output_file.write(f"Text: {char['text']}, Font: {char['fontname']}, Size: {char['size']}\n")


