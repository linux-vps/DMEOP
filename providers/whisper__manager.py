import os
import whisper
import torch
import requests
from tempfile import NamedTemporaryFile


def transcribe_audio(audio_url: str, task: str = "Transcribe", use_model: str = "tiny", language: str = "English") -> str:
    task = "transcribe" if task == "Transcribe" else "translate"
    
    # Download audio file from URL
    response = requests.get(audio_url)
    if response.status_code != 200:
        raise Exception(f"Failed to download audio file. Status code: {response.status_code}")
    
    # Save audio to a temporary file
    with NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
        temp_file.write(response.content)
        temp_audio_path = temp_file.name
    
    # Detect device
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    
    if DEVICE == "cuda":
        print("Using GPU")
    else:
        print("Using CPU")
    
    # Display language
    WHISPER_LANGUAGES = [k.title() for k in whisper.tokenizer.TO_LANGUAGE_CODE.keys()]
    
    if language == "Auto-Detect":
        language = "detect"
    if language and language != "detect" and language not in WHISPER_LANGUAGES:
        print(f"Language '{language}' is invalid")
        language = "detect"
    
    if language and language != "detect":
        print(f"Language: {language}")
    
    # Load model
    MODELS_WITH_ENGLISH_VERSION = ["tiny", "base", "small", "medium"]
    if language == "English" and use_model in MODELS_WITH_ENGLISH_VERSION:
        use_model += ".en"
    
    model = whisper.load_model(use_model, device=DEVICE)
    
    # Set options
    options = {
        'task': task,
        'verbose': True,
        'fp16': False,
        'best_of': 5,
        'beam_size': 5,
        'temperature': (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
        'condition_on_previous_text': False,
        'initial_prompt': None,
        'word_timestamps': False,
    }
    
    
    # Open-Source processing
    result = whisper.transcribe(model, temp_audio_path, **options)
    
    # Fix results formatting
    for segment in result['segments']:
        segment['text'] = segment['text'].strip()
    result['text'] = '\n'.join(map(lambda segment: segment['text'], result['segments']))
    
    # Clean up temporary file
    os.remove(temp_audio_path)
    transcribed_text = result['text'].replace(".", "").upper()
    
    # Return the transcribed text
    return transcribed_text