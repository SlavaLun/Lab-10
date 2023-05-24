import requests
import pyttsx3
import speech_recognition as sr
import os

# Инициализация голосового движка
engine = pyttsx3.init()

# Установка голоса
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Функция для преобразования текста в речь
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Функция для распознавания команды с использованием библиотеки Vosk
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Скажите команду:")
        audio = r.listen(source)
        try:
            text = r.recognize_vosk(audio, language='ru')  
            print("Вы сказали:", text)
            return text.lower()
        except sr.UnknownValueError:
            print("Не удалось распознать речь.")
            return ""
        except sr.RequestError as e:
            print("Ошибка сервиса распознавания речи:", str(e))
            return ""

# Функция для создания нового документа
def create_document():
    text = get_text()
    if text:
        with open("document.txt", "w") as file:
            file.write(text)
        speak("Новый документ создан.")

# Функция для чтения текста
def read_text():
    try:
        with open("document.txt", "r") as file:
            text = file.read()
        speak("Текст из документа:")
        speak(text)
    except FileNotFoundError:
        speak("Документ не найден.")

# Функция для сохранения текста как HTML
def save_as_html():
    try:
        with open("document.txt", "r") as file:
            text = file.read()
        with open("document.html", "w") as file:
            file.write("<html><body>")
            file.write("<p>" + text + "</p>")
            file.write("</body></html>")
        speak("Текст сохранен в формате HTML.")
    except FileNotFoundError:
        speak("Документ не найден.")

# Функция для сохранения текста без форматирования
def save_as_text():
    try:
        with open("document.txt", "r") as file:
            text = file.read()
        with open("document_plain.txt", "w") as file:
            file.write(text)
        speak("Текст сохранен без форматирования.")
    except FileNotFoundError:
        speak("Документ не найден.")

# Функция для получения текста с сайта
def get_text():
    try:
        response = requests.get('https://loripsum.net/api/10/short/headers')
        if response.status_code == 200:
            return response.text
        else:
            print("Ошибка при получении текста.")
            return ""
    except requests.RequestException as e:
        print("Ошибка при выполнении запроса:", str(e))
        return ""

# Основной цикл программы
while True:
    command = recognize_speech()

    if "создать" in command:
        speak("Создание нового документа.")
        create_document()

    elif "прочесть" in command:
        speak("Чтение текста.")
        read_text()

    elif "сохранить" in command:
        speak("Сохранение текста.")
        if "html" in command:
            save_as_html()
        else:
            save_as_text()

    elif "текст" in command:
        speak("Сохранение текста без форматирования.")
        save_as_text()

    else:
        speak("Неизвестная команда. Пожалуйста, повторите.")
