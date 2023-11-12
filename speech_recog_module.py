import speech_recognition as sr
from queue import Queue

def speech_recognition_thread(queue):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            audio = r.listen(source)
            try:
                command = r.recognize_google(audio)
                queue.put(command.lower())
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                pass
# def speech_recognition_thread(queue):
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         while True:
#             try:
#                 audio = r.listen(source, timeout=2)  # Adjust the timeout as needed
#                 command = r.recognize_google(audio)
#                 queue.put(command.lower())
#             except sr.UnknownValueError:
#                 pass
#             except sr.RequestError:
#                 pass
