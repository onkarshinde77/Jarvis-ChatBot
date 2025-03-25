import pygame
import random
import asyncio
import edge_tts
from dotenv import dotenv_values
import os

env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice", "en-US-JennyNeural")  # ✅ Set a default voice

async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3"
    
    if os.path.exists(file_path):
        os.remove(file_path)  # ✅ Fixed missing argument

    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
    await communicate.save(file_path)

def TTS(Text, func=lambda r=None: True):
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(TextToAudioFile(Text))  # ✅ Uses an existing event loop
        
        pygame.mixer.init()
        pygame.mixer.music.load(r'Data\speech.mp3')
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            if func() == False:
                break
            pygame.time.Clock().tick(10)
        return True
    except Exception as e:
        print(f"Error in TTS: {e}")
    finally:
        try:
            func(False)
            pygame.mixer.music.stop()
        except Exception as e:
            print(f"Error in finally block: {e}")
        pygame.mixer.quit()  # ✅ Quit mixer outside finally

def TextToSpeech(Text, func=lambda r=None: True):
    Data = [sentence for sentence in str(Text).split(".") if sentence.strip()]  # ✅ Removes empty sentences
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]
    
    if len(Data) > 4 and len(Text) >= 250:
        TTS(" ".join(Data[:2]) + ". " + random.choice(responses), func)  # ✅ Uses cleaned Data
    else:
        TTS(Text, func)

if __name__ == "__main__":
    while True:
        text = input("Enter the text: ")
        TextToSpeech(text)
