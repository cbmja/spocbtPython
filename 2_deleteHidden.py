import os
import shutil

# visibility:hidden -> visibility:visible
# visibility:hidden -> visibility:visible
# visibility:hidden -> visibility:visible

def update_html_visibility(input_dir, output_dir):
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".html"):
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, file_name)
            
            with open(input_path, "r", encoding="utf-8") as file:
                content = file.read()
            
            updated_content = content.replace('visibility:hidden', 'visibility:visible')
            
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(updated_content)
            
            print(f"Updated and saved: {output_path}")


input_dir = r"C:\Users\jeon\Desktop\온라인 자격증 시험\html변환\3. 워터마크 제거 후 html 변환 [ html ]"
output_dir = r"C:\Users\jeon\Desktop\온라인 자격증 시험\html변환\4. hidden 제거 [ html ]"

update_html_visibility(input_dir, output_dir)
