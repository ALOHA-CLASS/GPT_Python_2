import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
import subprocess
    
engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak(text):
    assistant_label.config(text=f"비서: {text}")
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        user_text = recognizer.recognize_google(audio, language='ko-KR')
        user_label.config(text=f"나: {user_text}")
        return user_text
    except sr.UnknownValueError:
        speak("죄송해요, 잘 알아듣지 못했어요.")
    except sr.RequestError:
        speak("서비스에 연결할 수 없어요.")
    return ""

def notify_time():
    now = datetime.datetime.now()
    msg = now.strftime("현재 시간은 %Y년 %m월 %d일 %H시 %M분 입니다.")
    messagebox.showinfo("시간 확인", msg)
    speak(msg)

def search_google():
    speak("무엇을 검색할까요?")
    query = recognize_speech()
    if query:
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"{query}에 대한 검색 결과를 보여드릴게요.")

def open_website():
    speak("어떤 웹사이트를 열까요? 구글, 유튜브, GPT 중에서 말씀해주세요.")
    keyword = recognize_speech()
    urls = {
        "구글": "https://www.google.com",
        "유튜브": "https://www.youtube.com",
        "GPT": "https://chat.openai.com"
    }
    if keyword in urls:
        webbrowser.open(urls[keyword])
        speak(f"{keyword}를 열게요.")
    else:
        speak("해당 웹사이트를 찾을 수 없어요.")

def run_program():
    speak("어떤 프로그램을 실행할까요? ZOOM 또는 VS CODE 중에서 말씀해주세요.")
    keyword = recognize_speech().upper()
    print("음성 : " + keyword)
    
    # 프로그램 경로 설정
    apps = {
        "ZOOM": "C:\\Users\\User\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe",
        "줌": "C:\\Users\\User\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe",
        "VS CODE": "C:\\Users\\User\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
        "VS 코드": "C:\\Users\\User\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    }
    
    # 키워드가 포함된 앱 찾기
    matched_apps = [app for app in apps if app.lower() in keyword.lower()]
    
    if matched_apps:
        # 일치하는 앱 실행
        subprocess.Popen(apps[matched_apps[0]])  # 첫 번째 일치 앱 실행
        speak(f"{matched_apps[0]}를 실행할게요.")
    else:
        speak("해당 프로그램을 찾을 수 없어요.")

def close_program():
    speak("어떤 프로그램을 종료할까요? 크롬, ZOOM, VS CODE 또는 앱 종료 중에서 말씀해주세요.")
    keyword = recognize_speech()
    
    # 종료할 프로그램들의 프로세스 이름 딕셔너리
    process_names = {
        "크롬": "chrome.exe",
        "Chrome": "chrome.exe",
        "ZOOM": "Zoom.exe",
        "줌": "Zoom.exe",
        "VS CODE": "Code.exe",
        "VS 코드": "Code.exe"
    }
    
    # 키워드가 포함된 프로세스 찾기
    matched_processes = [process for process in process_names if process.lower() in keyword.lower()]
    
    if keyword == "앱 종료":
        speak("비서 프로그램을 종료합니다.")
        root.destroy()
    elif matched_processes:
        for process in matched_processes:
            os.system(f"taskkill /f /im {process_names[process]}")
            speak(f"{process}를 종료했어요.")
    else:
        speak("해당 프로그램을 찾을 수 없어요.")


def memo():
    speak("메모를 말씀해주세요.")
    text = recognize_speech()
    if text:
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{now}_memo.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        speak("메모를 저장했어요.")

def process_command(command):
    if "시간" in command:
        notify_time()
    elif "검색" in command:
        search_google()
    elif "웹사이트" in command:
        open_website()
    elif "프로그램" in command:
        run_program()
    elif "종료" in command:
        close_program()
    elif "메모" in command:
        memo()
    else:
        speak("무슨 말씀인지 잘 모르겠어요.")

def on_voice_input():
    speak("무엇을 도와드릴까요?")
    command = recognize_speech()
    if command:
        process_command(command)

# GUI
root = tk.Tk()
root.title("음성인식 비서")
root.geometry("400x300")

label = tk.Label(root, text="음성인식 비서", font=("Arial", 16))
label.pack(pady=10)

btn_voice = tk.Button(root, text="음성인식", command=on_voice_input, font=("Arial", 14))
btn_voice.pack(pady=10)

assistant_label = tk.Label(root, text="비서: 대기 중...", font=("Arial", 20), fg="blue")
assistant_label.pack(pady=5)

user_label = tk.Label(root, text="나: 대기 중...", font=("Arial", 20), fg="green")
user_label.pack(pady=5)

root.mainloop()
