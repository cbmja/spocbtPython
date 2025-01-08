# -*- coding: utf-8 -*-

import os
import io
from collections import Counter
import numpy as np
import cv2
from PIL import Image
import fitz

# 원본 pdf 파일의 워터마크 제거
# 원본 pdf 파일의 워터마크 제거
# 원본 pdf 파일의 워터마크 제거

imgWidth = 3035

def deleteWatermark(pdf_dir, output_dir):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for pdf_file in os.listdir(pdf_dir):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, pdf_file)
            doc = fitz.open(pdf_path)
            page_cnt = len(doc)

            for page_index in range(page_cnt):
                page = doc[page_index]
                img_info = page.get_image_info(xrefs=True)

                for info in img_info:
                    xref = info['xref']
                    base_image = doc.extract_image(xref)
                    if imgWidth > 0 and base_image["height"] > 0:
                        x0, _, _, _ = info['bbox']
                        if x0 == 0.0 and base_image["width"] > imgWidth:
                            page.delete_image(xref)
                            continue

                        image = Image.open(io.BytesIO(base_image["image"]))
                        pil_array = np.array(image)
                        cv_image = cv2.cvtColor(pil_array, cv2.COLOR_RGB2BGR)
                        pixels = cv_image.reshape(-1, 3)
                        color_counts = Counter(tuple(pixel) for pixel in pixels)
                        most_common_colors = color_counts.most_common()
                        color_cnt = len(most_common_colors)
                        if base_image["width"] == 1 and base_image["height"] == 1 and color_cnt == 1:
                            page.delete_image(xref)

            output_path = os.path.join(output_dir, pdf_file)
            doc.save(output_path)
            doc.close()
            print(f"Processed and saved: {output_path}")

# 경로 설정
input_dir = r"C:\Users\jeon\Desktop\온라인 자격증 시험\html변환 시연\1. 원본 [ pdf ]"
output_dir = r"C:\Users\jeon\Desktop\온라인 자격증 시험\html변환 시연\2. 워터마크 제거 [ pdf ]"

deleteWatermark(input_dir, output_dir)

