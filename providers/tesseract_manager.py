import re, base64, io, pytesseract
from PIL import Image, ImageTk

def ocr(input_elements):
    answers = []
        
    for input_element in input_elements:
        style_attr = input_element.get_attribute("style")
        base64_string = re.search(r"base64,(.*)", style_attr).group(1)
        image_data = base64.b64decode(base64_string)
        image_bytes = io.BytesIO(image_data)
        image = Image.open(image_bytes)

        # Kích thước mới
        new_width = image.width * 2
        new_height = image.height * 2

        # Chuyển phóng to ảnh  
        zoom = image.resize((new_width, new_height))

        zoom_bytes = io.BytesIO()
        zoom.save(zoom_bytes, format='PNG')
        zoom_bytes.seek(0)
        
        answer = pytesseract.image_to_string(zoom, lang='eng', config = '--psm 1 --psm 10 ')
        # answer = response.text   
        answer = answer.replace("|", "I") 
        answer = answer.replace("Cc", "c")
        if answer == "9":
            # Kiểm tra xem tất cả các phần tử của answers có phải là ký tự số không
            all_digits = all(answerTest.isdigit() for answerTest in answers)
            # Kiểm tra xem nếu chỉ có một ký tự thì mới xử lý
            if all_digits and all(len(answerTest) == 1 for answerTest in answers):
                # Nếu tất cả đều là số và chỉ có một ký tự, thay thế "g" thành "9"
                answer.replace("g", "9")
            elif not all_digits and all(len(answerTest) == 1 for answerTest in answers):
                # Nếu không phải tất cả là số và chỉ có một ký tự, thay thế "9" thành "g"
                answer.replace("9", "g")
        answers.append(answer)
    return answers