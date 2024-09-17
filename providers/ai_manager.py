from g4f.client import Client
import time
# Biến cục bộ:
client = Client()
chat_history = []


def ask_ai(task_type, question, audio_type=None, wrongAnswers=None):
    try:
        if wrongAnswers:
            print(wrongAnswers)
        addTextPrompt = ""
        if ",  ," in question:
            addTextPrompt = "If the resulting word has synonyms, include both and separate them with ' / '."
            if "characters" in question:
                addTextPrompt = ""
                if "whisperResponsed" in question:
                    addTextPrompt = "If the resulting word has synonyms, include both and separate them with ' / '."
        if task_type == "pronunciation":
            prompt = f"""
            Rearrange the characters to match the letters created from the phonetic transcription. neither redundant nor lacking.
            Only answer the target word. (not Output: ...)
            {addTextPrompt}
            Avoid repeating the following wrong answers {wrongAnswers}

            input: /weə(r) aʊt/
            W, , A, E, T, O, R, U
            output: WEAR OUT

            input: /ˈsiːlənt/
            A, A, E, L, N, S, T 
            output: SEALANT 

            input: {question}
            output:
        """
            response = ai_response(prompt)
            response = response.upper()
            return response
        elif task_type == "audio":
            if audio_type == "reorderAudioAi":
                prompt = f"""The word must use all listed characters: {question}
                Rearrange the characters to match the meaningful words. neither redundant nor lacking.
                Only answer the target word. (not Output: ...)
                {addTextPrompt}
                Avoid repeating the following wrong answers {wrongAnswers}

                input: GRAPHICS PROCESSING UNIT.
                output: GRAPHICS PROCESSING UNIT 

                input: HEAD OFFICE HEADQUARTERS.
                output: HEAD OFFICE / HEADQUARTERS

                input: {question}
                output:
            """
                response = ai_response(prompt)
                response = response.upper()
                return response
            elif audio_type == "reorderAudioWhisperThenAi":
                prompt = f"""
                You will assist me in finding the correct word based on the result from Whisper. 
                The result from Whisper is only a suggestion and may be partially correct or incorrect. 
                The final word must be constructed using the provided letters, and the Whisper result should only guide the process, not dictate the exact word.

                Rearrange the characters to match the meaningful words. neither redundant nor lacking.
                Only answer the target word. (not Output: ...)
                {addTextPrompt}
                Avoid repeating the following wrong answers {wrongAnswers}

                Input: [
                        whisper: SEALANT
                        characters: N, S, A, E, T, L, A
                    ]
                Output: SEALANT

                Input: [
                        whisper: HEAD OFFICE HEADQUARTERS
                        characters: R, I, F, A, A, T,  , C, O, U, D,  , Q, A, E, E, D, E, H, E, R, F, S, H
                    ]
                Output: HEAD OFFICE / HEADQUARTERS

                Input: {question}
                Output: ?
                """
                response = ai_response(prompt)
                response = response.upper()
                return response
        elif task_type == "fix_wrong_answer":
            prompt = f""" 
            You will receive an incorrect line of text or a word, which may have a few words wrong due to minor errors in reading the text from the image.
            Do not add or remove any words.
            If it is "WWW", change it to "W".
            When converting photos to text, there might be instances where the letter 'n' between words is mistakenly interpreted as 'h.' Please review it and make corrections if needed.
            Do not arbitrarily add words or accents, just guess and correct the wrong character.
            Every word in the sentence must be correct. Do not edit specialized abbreviations.
            Sometimes, words get stuck together, for example, the correct word should be "a router" but is incorrectly written as "arouter". 
            If there are few characters, the answer is a character in multiple-choice questions; 
            Just reply to me with edited text, nothing more.
            Please correct it and send the text back to me. Just send the text back, nothing more.

            ***
            incorrect line of text: "{question}"
            """
            response = ai_response(prompt)
            return response
    except Exception as e:
        print(f"Error in ask_ai function: {str(e)}")


def ai_response(question):
    global chat_history

    try:
        chat_history.append({"role": "user", "content": question})

        if len(chat_history) > 8:
            chat_history = chat_history[-8:]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_history
        )

        final_text = response.choices[0].message.content
        final_text = final_text.replace(".", "").upper()
        
        if "SORRY" in final_text:
            print("Chờ 50 giây để sử dụng AI")
            time.sleep(50)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=chat_history
            )

            final_text = response.choices[0].message.content
            final_text = final_text.replace(".", "").upper()
            final_text = final_text.replace("OUTPUT: ", "")
            if "SORRY" in final_text:
                final_text = " "

        time.sleep(2)
        chat_history.append({"role": "assistant", "content": response.choices[0].message.content})
        return final_text

    except Exception as e:
        print(f"Error in ai_response function: {str(e)}")
        return None
        
# 17/09/2024
# https://github.com/linux-vps
# https://www.facebook.com/groups/1493850704586284
