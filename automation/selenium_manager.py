from selenium.webdriver.common.action_chains import ActionChains
import random
import time
from selenium.webdriver.support.ui import WebDriverWait 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from providers.ai_manager import ask_ai
from providers.tesseract_manager import ocr
from providers.whisper__manager import transcribe_audio

import traceback

def insertScript(driver):
    # Chèn mã JavaScript để in giá trị của biến dgt ra console
    script = """
    var checkVisible = setInterval(function() {
        var closeModalBtn = document.querySelector('body > div.modal.fade.dgmodal.in > div > div > div.modal-footer > button');
        
        // Kiểm tra nếu button tồn tại và modal hiển thị
        if (closeModalBtn && closeModalBtn.offsetParent !== null) {
            closeModalBtn.click();  // Click để đóng modal
        }
    }, 50);  // Kiểm tra mỗi 50ms
    var checkVisible = setInterval(function() {
        var closeModalBtn = document.querySelector('body > div.dboxy.fixed > div > div > b.dbxclo');
        
        // Kiểm tra nếu button tồn tại và modal hiển thị
        if (closeModalBtn && closeModalBtn.offsetParent !== null) {
            closeModalBtn.click();  // Click để đóng modal
        }
    }, 50);  // Kiểm tra mỗi 50ms
    """

    # Thực hiện chèn mã JavaScript vào trang web
    driver.execute_script(script)  
    

def getTaskType(driver):
    time.sleep(1)
    first_element = driver.find_element(By.ID, "mbody").find_elements(By.TAG_NAME, "div")[0]
    element_class = first_element.get_attribute("class")
    taskType = element_class.split(" ")[0]
    return element_class, taskType

def open_browser():
    options = Options()
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-notifications')
    options.add_argument('--start-maximized')
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(options=options)
    
    return driver

# Hàm đăng nhập
def login(driver, username, password):
    # Lấy thông tin đăng nhập
    
    # Truy cập trang đăng nhập
    driver.get("https://eop.edu.vn/base/login")
    
    
    # Tìm và điền thông tin vào form
    username_field = driver.find_element(By.ID, "input-username")
    password_field = driver.find_element(By.ID, "input-password")
    
    # Xử lý ngoại lệ
    try:
        username_field.clear()
        password_field.clear()
    except:
        return
    # Điền thông tin và submit
    username_field.send_keys(username) 
    password_field.send_keys(password)
    login_button = driver.find_element(By.ID, "login-btn")
    login_button.click()
    
# Hàm kiểm tra đăng nhập thành công    
def check_login(driver):
    try:
        # Đợi 10 giây cho phần tử có id davatar xuất hiện
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "davatar"))
        )
        return True     
    except:
        return False

def submit(driver):
    try:
        time.sleep(3)  # Đợi 3 giây trước khi thực hiện tiếp
        try:
            done_button = driver.find_element(By.CSS_SELECTOR, "#mfooter > button")
            actions = ActionChains(driver)
            actions.move_to_element(done_button).click(done_button).perform()
        except:
            close_modal_btn = driver.find_element(By.XPATH, 'body > div.modal.fade.dgmodal.in > div > div > div.modal-footer > button')
            close_modal_btn.click()
        # Chờ cho phần tử có class là "loading" biến mất s
        wait = WebDriverWait(driver, 30)
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading")))
        doneTask = driver.execute_script("""return document.querySelector('#daudioplayer').src;""")
        if doneTask == 'https://i.eop.edu.vn/rs/success0.wav':
            print("Ấn nút hoàn thành")
            time.sleep(3)
            pass
        if doneTask == 'http:////i.eop.edu.vn/rs/congratulations0.mp3':
            print("Ấn nút hoàn thành")
            time.sleep(3)
            pass
        else:
            print("Ấn nút hoàn thành")
            time.sleep(3)   
            pass 
        time.sleep(4)
    except:
        print("\n#################################################\n")
        time.sleep(3)
        pass
    pass

# Bài từ vựng đầu tiên
def getVocabulary(driver):
    print("\nBài đầu tiên\n")
    buttons = driver.find_elements(By.CLASS_NAME, "fa-play-circle.daudio") # Tìm tất cả các nút có class là "fa fa-play-circle daudio"
    print(f"\nTổng cộng có {len(buttons)} từ vựng.")
    for button in buttons:                          # Lặp qua từng nút và ấn vào chúng lần lượt
        button.click()
    time.sleep(1)                                # Đợi 1 giây trước khi thực hiện tiếp
    submit(driver)
    pass


# Bài chọn từ vựng
def select(driver):
    try:
        print("\nĐây là bài chọn từ vựng")
        # Chờ cho tới khi phần tử chứa class 'dvoca q... active' xuất hiện trong DOM
        wait = WebDriverWait(driver, 10)
        active_question = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class*="dvoca q"][class*="active"]')))
        answer_list = active_question.find_elements(By.CLASS_NAME, "dans")
        time.sleep(5)
        for div in answer_list:
            title = div.find_element(By.CLASS_NAME, "dtitle")
            title.click()
            time.sleep(3)
        time.sleep(1.5)
        submit(driver)
    except:
        pass
# Hàm lấy danh sách từ vựng của unit
def get_vocab_list(driver):
    # Lấy từ vựng và phiên âm
    try:
        unit_tasks = WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.ID, "tpvocabulary")))
        Vocabulary_Presentation_vocabulary= unit_tasks.find_element(By.CLASS_NAME, "dpop.allow.vocabulary.dgtaskdone")
        url = Vocabulary_Presentation_vocabulary.get_attribute("href")
        # Trường hợp có nhiều bài từ vựng, tức không chỉ 1 bài thì nên lấy bằng đấy từ vựng và lưu vào 1 danh sách. VD. Nick a Toàn Tiếng Anh 1 Unit 5 có 3 bài từ vựng.
        # Lấy cookies của webdriver ban đầu
        cookies = driver.get_cookies()
        # Khởi tạo một instance webdriver mới
        options = Options()
        options.headless = True
        options.add_argument('--disable-notifications')
        options.add_argument("--headless=new")
        options.add_argument('--disable-infobars')
        options.add_argument('--start-maximized')
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        new_driver = webdriver.Chrome(options=options)
        # Truy cập đến một URL bất kì
        new_driver.get("https://eop.edu.vn/base/login")
        # Chuyển toàn bộ cookies
        for cookie in cookies:
            new_driver.add_cookie(cookie)
        # Truy cập trang với WebDriver mới này
        new_driver.get(url)
        # Tìm tất cả các thẻ có class "ditem"
        items = new_driver.find_elements(By.CLASS_NAME, "ditem")
        # Danh sách kết quả chứa các cặp (từ, url âm thanh)
        vocab_list = []
        # Duyệt qua từng thẻ "ditem"
        for item in items:
            # Lấy url file âm thanh từ thẻ i có class "daudio"
            audio_url = item.find_element(By.CSS_SELECTOR, "i.daudio").get_attribute('media-url')
            # Lấy từ vựng từ thẻ <h4>
            word = item.find_element(By.TAG_NAME, "h4").text.strip()
            # Thêm cặp (từ, phiên âm) vào kết quả
            vocab_list.append((word, audio_url))
        new_driver.quit()
        print("\nĐã lấy từ vựng của Unit này\n")
        return vocab_list
 
    except:
        print("\n\nCấu trúc Unit này chưa được train, không lấy được từ vựng\n\n")
        pass

# Bài chọn trắc nghiệm
def multipleChoice(driver):
    print("\nĐây là bài trắc nghiệm")
    questions = driver.find_elements(By.CLASS_NAME, "ques")
    first_question = questions[0]
    dchk = first_question.find_elements(By.CSS_SELECTOR, "div p label")
    num_answers = len(dchk)
    for i in range(num_answers):
        for question in questions:
            answers = question.find_elements(By.CSS_SELECTOR, "div p label")
            found = False
            for answer in answers:
                if answer.get_attribute("style") == "color: green;":
                    found = True
                    break
            if found:
                continue
            if len(answers) > i:
                click_ans = answers[i]
                click_ans.click()        
        submit(driver)
        continue
    pass

def analizeReorderTask(driver, vocab_list):
    # Sắp xếp từ vựng
    print("\nSắp xếp từ vựng\n")
    wait = WebDriverWait(driver, 10)
    active_question = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class*="dvoca q"][class*="active"]')))
    
    # Kiểm tra xem ul.dview.sortable có phần tử <li> nào không
    try:
        li_elements = active_question.find_elements(By.CSS_SELECTOR, 'ul.dview.sortable li')
        if not li_elements:
            print("")
        
        # Nếu có phần tử, click vào chúng lần lượt
        for li in li_elements:
            li.click()

        # Lấy danh sách phần tử <li> từ phần tử <ul> có class 'dstore sortable', lưu kết quả li đi kèm với text trong một danh sách
        li_elements = [(el.text, el) for el in active_question.find_elements(By.CSS_SELECTOR, 'ul.dstore.sortable li')]
        # Lưu kết quả li đi kèm với text trong một danh sách
        letters = ", ".join(item[0] for item in li_elements)
        
        current_question, total_questions, question_info = getCurrentQuestions(driver)
        print(f'Tổng số câu hỏi: {total_questions}')
        print(f"Question {question_info}")
        
        # Lấy url âm thanh của đề bài
        media_url = active_question.find_element(By.CSS_SELECTOR, "i.daudio").get_attribute('media-url')
        target_word = None
        for word, audio_url in vocab_list:
            # So sánh url âm thanh của đề bài với audio_url trong mỗi cặp (từ - url)
            if media_url == audio_url:
                # Nếu trùng, gán target word
                target_word = word.upper()
                print("\nTìm thấy từ vựng trong danh sách Vocab_list\n")
                break
        
        return li_elements, target_word, media_url, letters, current_question
    
    except Exception as e:
        print("Đã xảy ra lỗi: ")
        traceback.print_exc()
        print(f"Lỗi chi tiết: {str(e)}")
        return [], None, None


def getCurrentQuestions(driver):
    # Lấy số câu
    time.sleep(2)
    wait = WebDriverWait(driver, 10)
    active_question = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class*="dvoca q"][class*="active"]')))
    li_elements = active_question.find_elements(By.CSS_SELECTOR, 'ul.dview.sortable li')
    if not li_elements:
        print("")
    else:
        # Nếu có phần tử, click vào chúng lần lượt
        print("Làm lại")
        for li in li_elements:
            li.click()
    time.sleep(2)
    question_text_element = active_question.find_element(By.CLASS_NAME, "dqtit")
    question_text = question_text_element.text  # 'Question 1/34:'
    
    # Tách chuỗi và lấy ra số thứ tự và tổng số câu hỏi
    _, question_info = question_text.split('Question ')
    current_question, total_questions = question_info.split('/')
    
    # Loại bỏ dấu hai chấm từ total_questions
    total_questions = total_questions[:-1]
    
    # Ép kiểu về int để tiện xử lý
    current_question = int(current_question)
    total_questions = int(total_questions)
    print(f"Question {question_info}")
    return current_question, total_questions, question_info

def click_reorder(driver, target_word, li_elements, current_question0):
    try:
        for word in target_word:
            for char in word:
                if char == " ":
                    # Nếu là khoảng trắng, tìm danh mục li chứa khoảng trắng click.
                    for i, (text, li) in enumerate(li_elements):
                        if text == "":
                            li.click()
                            WebDriverWait(driver, 10).until(EC.staleness_of(li))
                            # sau khi click, xóa ký tự này khỏi danh sách
                            del li_elements[i]
                            break
                else:
                    # Nếu không phải khoảng trắng. Tìm và click vào phần tử li chứa ký tự tương ứng.
                    for i, (text, li) in enumerate(li_elements):
                        if text == char:
                            li.click()
                            WebDriverWait(driver, 10).until(EC.staleness_of(li))
                            # sau khi click, xóa ký tự này khỏi danh sách
                            del li_elements[i]
                            break        
                
        time.sleep(0.5)
        current_question, total_questions, question_info = getCurrentQuestions(driver)
        if current_question != current_question0:
            return True
        else:
            return False
    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred during the reorder process: {str(e)}")
        return False

def pronunciation_reorder_OpenAI(driver, letters, wrongAnswers):
    try:
        # Chờ cho tới khi phần tử chứa class 'dvoca q... active' xuất hiện trong DOM
        wait = WebDriverWait(driver, 10)
        active_question = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class*="dvoca q"][class*="active"]')))
        
        # Lấy đề bài của câu

        target_spelling = active_question.find_element(By.CLASS_NAME, 'title').text

        
        # Chờ cho tới khi phần tử chứa class 'dvoca q... active' xuất hiện trong DOM
        wait = WebDriverWait(driver, 10)
        active_question = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class*="dvoca q"][class*="active"]')))
        
        input_prompt = f'{target_spelling} \n {letters}'
        response = ask_ai('pronunciation', input_prompt, audio_type=None, wrongAnswers=wrongAnswers)
        response = response.upper()
        return response
    except Exception as e:
        # In lỗi và chi tiết lỗi ra console
        print(f"Lỗi chi tiết: {str(e)}")
        
def reorderAudioWhisper(media_url):
    try:
        # URL of the file to transcribe
        FILE_URL = f"""https:{media_url}"""
        transcribed_text = transcribe_audio(FILE_URL)
        transcribed_text = transcribed_text.upper()
        return transcribed_text
    except:
        print("Đã xảy ra lỗi: reorderAudioWhisper")
def reorderAudioWhisperThenAi(media_url, letters, wrongAnswers):
    try:
        # URL of the file to transcribe
        FILE_URL = f"""https:{media_url}"""
        transcribed_text = transcribe_audio(FILE_URL)
        transcribed_text = transcribed_text.upper()
        input_prompt = f"""
            [
                whisperResponse: {transcribed_text},
                characters: {letters}
            ]
            """
        if ",  ," in letters:
            input_prompt = f"""
            [
                whisperResponsed: {transcribed_text},
                characters: {letters}
            ]"""
            

        response = ask_ai('audio', input_prompt, audio_type='reorderAudioWhisperThenAi', wrongAnswers=wrongAnswers)
        response = response.upper()
        return response
    except:
        print("Đã xảy ra lỗi: reorderAudioWhisperThenAi")
def reorderAudioAi(letters, wrongAnswers):
    try:
        response = ask_ai('audio', letters, audio_type='reorderAudioAi', wrongAnswers=wrongAnswers)
        response = response.upper() 
        return response
    except:
        print("Đã xảy ra lỗi: reorderAudioAi")
    
import traceback

def normal(driver, randomFrom, randomTo):
    print("\nBài bình thường\n")
    print(f"randomFrom: {randomFrom}")
    print(f"randomTo: {randomTo}")
    # Đảm bảo rằng randomFrom và randomTo là số nguyên
    if not isinstance(randomFrom, int):
        randomFrom = int(randomFrom)
    if not isinstance(randomTo, int):
        randomTo = int(randomTo)
    
    try:
        empty_input_elements = driver.find_elements(By.CSS_SELECTOR, "#dquestion input")
        # Điền sai đáp án vào các input 3 lần cho chắc 
        for empty_input_element in empty_input_elements:
            empty_input_element.send_keys("Bánh Đậu ")
        for empty_input_element in empty_input_elements:
            empty_input_element.send_keys("Xanh")
        
        # Click nút hoàn thành
        time.sleep(4)
        driver.find_element(By.CSS_SELECTOR, "#mfooter > button").click()
        
        # Chờ để Click nút xem đáp án
        time.sleep(32)
        driver.find_element(By.CSS_SELECTOR, "#mfooter > button").find_element(By.XPATH, "following-sibling::*").click()
        time.sleep(3)
        
        input_elements = driver.find_elements(By.CSS_SELECTOR, "#dquestion input")
        answers = ocr(input_elements)
        
        # Click nút làm lại
        driver.find_element(By.CSS_SELECTOR, "#mfooter > button").find_element(By.XPATH, "following-sibling::*").click()

        # Điền đáp án
        for i in range(len(input_elements)):
            input_element = input_elements[i]
            input_element.clear()
            input_element.send_keys(answers[i])
        
        # Chờ thời gian ngẫu nhiên random time
        timeToSleep = random.randint(randomFrom,randomTo)
        print(timeToSleep)
        time.sleep(timeToSleep)

        submit(driver)
        
        # Nếu có sai sót
        # Cách đang sáng tạo
        mbody = WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.ID, "mbody")))
        dhelptext = mbody.find_element(By.CLASS_NAME, 'dhelp').get_attribute("textContent")
        time.sleep(5)

        filled_input_elements = driver.find_elements(By.CSS_SELECTOR, "#dquestion input")
        for i, input_element in enumerate(filled_input_elements):
            if 'color: red' in input_element.get_attribute('style'):
                concatenated_string = ""
                index = i
                answer = answers[i]
                p_tag = input_element.find_element(By.XPATH, "..")
                p_tag_text = p_tag.text
                concatenated_string += p_tag_text + "\n\n=> " + answer
                prompt = ""
                prompt += dhelptext + "\n\n" + "fix this answer\n" + concatenated_string
                print(prompt)

        # Cách đang dùng
        try:
            filled_input_elements = driver.find_elements(By.CSS_SELECTOR, "#dquestion input")
            for i, input_element in enumerate(filled_input_elements):
                if 'color: red' in input_element.get_attribute('style'):
                    index = i
                    answer = answers[i]
                    print(f"\nĐang sửa đáp án sai do lỗi nhận diễn chữ từ ảnh: {answer}\n")
                    fixed_input = ask_ai('fix_wrong_answer', answer, audio_type=None, wrongAnswers=None)
                    print(f"\nĐã sửa thành: \t\t\t{fixed_input}\n")
                    input_element.clear()
                    input_element.send_keys(fixed_input)
                    submit(driver)
        except Exception as e:
            print("Lỗi phần sửa đáp án sai: ")
            traceback.print_exc()
            print(f"Lỗi chi tiết: {str(e)}")

    except Exception as e:
        print("Đã xảy ra lỗi: ")
        traceback.print_exc()
        print(f"Lỗi chi tiết: {str(e)}")
