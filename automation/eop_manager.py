from .selenium_manager import *
import time
import sys
from pathlib import Path
# Thêm thư mục gốc vào sys.path
sys.path.append(str(Path(__file__).parent.parent))

def typeTask(driver, vocab_list, randomFrom, randomTo):
    insertScript(driver)
    vocab_list = vocab_list
    while True:
        element_class, taskType = getTaskType(driver)
        # try:
        if taskType == 'dvocabulary':
            getVocabulary(driver)
            break
        if  taskType == 'dmcq':
            
            if "write" in element_class:
                reorder(driver, vocab_list, element_class)

                break
            else:
                select(driver)
                break
        if taskType == "dquestion":
            if "choose" in element_class:
                multipleChoice(driver)
                break
            else:
                normal(driver, randomFrom, randomTo)
                break
        if taskType == "dcontent":
            submit(driver)
            break
        
# Bài sắp xếp từ vựng
def reorder(driver, vocab_list, element_class):
    li_elements, target_word, media_url, letters, current_question = analizeReorderTask(driver, vocab_list)
    # Kiểm tra xem có phải dạng nhìn phiên âm viết lại từ không
    if target_word == None: 
        wrongAnswers = []
        if(element_class=="dmcq audio-write-word"):
            print("\nDạng bài nghe rồi sắp xếp lại từ")
            target_word2 = reorderAudioWhisper(media_url)
            taskPassed1 = click_reorder(driver, target_word2, li_elements, current_question) 
            time.sleep(1)
            if taskPassed1:
                print("Passed")
            else:
                wrongAnswers.append(target_word2)
                for i in range(1, 6):
                    li_elements, target_word, media_url, letters, current_question = analizeReorderTask(driver, vocab_list)
                    target_word3 = reorderAudioAi(letters, wrongAnswers)
                    taskPassed2 = click_reorder(driver, target_word3, li_elements, current_question) 
                    time.sleep(1)
                    if taskPassed2:
                        print("Passed")
                        break
                    else:
                        li_elements, target_word, media_url, letters, current_question = analizeReorderTask(driver, vocab_list)
                        wrongAnswers.append(target_word3)
                        target_word4 = reorderAudioWhisperThenAi(media_url, letters, wrongAnswers)
                        taskPassed3 = click_reorder(driver, target_word4, li_elements, current_question) 
                        time.sleep(1)
                        if taskPassed3:
                            print("Passed")
                            break
                        else:
                            wrongAnswers.append(target_word4)
                        
        elif (element_class=="dmcq pronunciation-write-word"):
            for i in range(1, 6):
                li_elements, target_word, media_url, letters, current_question = analizeReorderTask(driver, vocab_list)
                target_word5 = pronunciation_reorder_OpenAI(driver, letters, wrongAnswers)
                taskPassed = click_reorder(driver, target_word5, li_elements, current_question) 
                if taskPassed:
                    print("Passed")
                    break
                else:
                    wrongAnswers.append(target_word5)

            
    
        
    time.sleep(1)
    

def main(username, password, randomFrom, randomTo):
    # Gọi hàm mở trình duyệt
    driver = open_browser()  
    login(driver, username, password)
    if check_login(driver):
        vocab_list = get_vocab_list(driver)
        while True: 
            try:
                typeTask(driver, vocab_list, randomFrom, randomTo)
            except:
                print("\n\nChưa phân loại dạng bài được\n\n")
                continue
            
