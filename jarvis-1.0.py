import pyttsx3 # pip install pyttsx3
import datetime
import speech_recognition as sr # pip install speechRecognition
import wikipedia # pip install wikipedia
import smtplib
import webbrowser as wb
import psutil # pip install psutil
import pyjokes # pip install pyjokes
import os
import pyautogui # pip install pyautogui
import random
import wolframalpha # pip install wolframalpha
import json
import requests
from urllib.request import urlopen
import time

engine = pyttsx3.init()
wolframalpha_app_id = "QK6X2W-8QLW97U5EH"
wikipedia.set_lang('es')

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time_():
    _time_ = datetime.datetime.now().strftime("%I:%M:%S") # for 12 hour clock
    speak("La hora actual es")
    speak(_time_)

def date_():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day

    speak("La fecha actual es")
    speak(day)

    switcher = {
        1: " de Enero de",
        2: "de Febrero de",
        3: "de Marzo de",
        4: "de Abril de",
        5: "de Mayo de",
        6: "de Junio de",
        7: "de Julio de",
        8: "de Agosto de",
        9: "de Septiembre de",
        10: "de Octubre de",
        11: "de Noviembre de",
        12: "de Diciembre de"
    }
    speak(switcher.get(month, "Invalid month"))
    speak(year)

def wishme():
    speak("Hola de nuevo familia Varela")
    time_()
    date_()

    # Greetings
    hour = datetime.datetime.now().hour

    if hour >= 6 and hour < 12:
        speak("Buenos días familia")
    elif hour >= 12 and hour < 18:
        speak("Buenas tardes familia")
    elif hour >= 18 and hour < 24:
        speak("Buenas noches familia")
    else:
        speak("Buenas noches familia")
    speak("Jarvis está a su servicio, Por favor diganme, ¿cómo puedo ayudarlos hoy?")

def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Reconociendo...")
        query = r.recognize_google(audio, language = "es-CO")
        print(query)
    except Exception as e:
        print(e)
        print("Repite la frase por favor...")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()

    # fot his function, you must enable low security in you gmail with you are going to use as sender
    server.login("cursosubidos2@gmail.com", "")
    server.sendmail("cursosubidos2@gmail.com", to, content)
    server.close()

def screenshot():
    img = pyautogui.screenshot()
    img.save("C:/Users/Usuario/Pictures/Jarvis")

def cpu():
    usage = str(psutil.cpu_percent())
    speak("La CPU esta en" + usage)
    battery = psutil.sensors_battery()
    
    if battery is None:
        speak("Este dispositivo no tiene bateria integrada")
    else:
        speak("La bateria esta en")
        speak(battery.percent)

def joke():
    speak(pyjokes.get_joke(language = "es", category = "all"))

if __name__ == "__main__":
    wishme()

    while True:
        query = TakeCommand().lower()

        # All commands will be stored in lower case in query for easy recognition

        if "hora" in query: # Tell us time when asked
            time_()
        
        elif "fecha" in query: #tell us date when asked
            date_()

        elif "wikipedia" in query:
            speak("Buscando...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences = 3)
            speak("En base a Wikipedia")
            #print(result)
            speak(result)

        elif "enviar mensaje" in query:
            try:
                speak("Que debo decir?")
                content = TakeCommand()

                #provide reciever email address
                speak("A quien debo enviar el mensaje?")
                reciever = input("Ingrese el email del destinatario: ")
                to = reciever
                sendEmail(to, content)
                speak(content)
                speak("El mensaje fue enviado")
            except Exception as e:
                print(e)
                speak("Envio fallido")

        elif "buscar en chrome" in query:
            speak("Que desea que busque?")
            chromepath = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
            # chromepath is location of chrome's installation on Computer

            search = TakeCommand().lower()
            wb.get(chromepath).open_new_tab(search + ".com") #only open websites with '.com' at end
        
        elif "buscar en youtube" in query:
            speak("Que video desea que busque?")
            search_Term = TakeCommand().lower()
            speak("Abriendo YouTube")
            wb.open("https://www.youtube.com/results?search_query=" + search_Term)

        elif "buscar en google" in query:
            speak("Que desea que busque?")
            searchTerm = TakeCommand().lower()
            speak("Buscando...")
            wb.open("https://www.google.com/search?q=" + searchTerm)

        elif "cpu" in query:
            cpu()

        elif "chiste" in query:
            joke()

        elif "offline" in query:
            speak("Desactivando sistema")
            quit()

        elif "abrir word" in query:
            speak("Abriendo Microsoft Word")
            ms_word = r"C:/Program Files/Microsoft Office/root/Office16/WINWORD.EXE"
            os.startfile(ms_word)

        elif "escribir una nota" in query:
            speak("Que desea que escriba?")
            notes = TakeCommand()
            file = open("notes.txt", "w")
            speak("Desea que incluya la fecha y hora?")
            ans = TakeCommand().lower()

            if "si" in ans or "claro" in ans:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(":-")
                file.write(notes)
                speak("Notas guardadas")
            else:
                file.write(notes)

        elif "mostrar nota" in query:
            speak("Mostrando notas")
            file = open("notes.txt", "r")
            speak(file.read())

        elif "captura de pantalla" in query:
            screenshot()

        elif "música" in query:
            songs_dir = "F:/Musica Cristiana"
            music = os.listdir(songs_dir)
            speak("Que cancion quiere que reproduzca?")
            speak("Selecciona un numero...")
            ans = TakeCommand().lower()

            while("número" not in ans and ans != "aleatorio" and ans != "elige tú"):
                speak("No logro entenderte, intenta de nuevo")
                ans = TakeCommand().lower()
            if "número" in ans:
                num = int(ans.replace("número", ""))
            elif "aleatorio" in ans or "elige tú" in ans:
                num = random.randint(1, 53)
            os.startfile(os.path.join(songs_dir, music[num]))
                

        elif "guardar recordatorio" in query:
            speak("Que debo recordar?")
            memory = TakeCommand()
            speak("Me solicito que recuerde lo siguiente: " + memory)
            remember = open("memory.txt", "w")
            remember.write(memory)
            remember.close()

        elif "hay algún recordatorio" in query:
            remember = open("memory.txt", "r")
            speak("Me solicito que recordara lo siguiente: " + remember.read())

        elif "noticias" in query:
            try:
                jsonObj = urlopen("http://newsapi.org/v2/top-headlines?country=us&category=entertainment&apiKey=25934dd21a5848acbbfc32ca3b643683")
                data = json.load(jsonObj)
                i = 1

                speak("Aqui hay algunas de las mejores noticias de entretenimiento")

                for item in data["articles"]:
                    print(str(i) + ". " + str(item["title"]) + "\n")
                    print(str(item["description"]) + "\n")
                    speak(item["title"])
                    i += 1

            except Exception as e:
                print(str(e))

        elif "dónde está" in query:
            query = query.replace("dónde está", "")
            location = query
            speak("Me solicitó que localizara " + location)
            wb.open_new_tab("https://www.google.com/maps/place/" + location)

        elif "calcular" in query:
            client = wolframalpha.Client(wolframalpha_app_id)
            indx = query.lower().split().index("calcular")
            query = query.split()[indx + 1:]
            res = client.query("".join(query))
            answer = next(res.results).text
            speak("La respuesta es " + answer)

        elif "qué es" in query or "quién es" in query:
            # use the same API key that we generated earlier i.e. wolframalpha
            client = wolframalpha.Client(wolframalpha_app_id)

            if "qué es" in query:
                query = query.replace("qué es", "what is")
            elif "quién es" in query:
                query = query.replace("quién es", "who is")

            res = client.query(query)

            try:
                print(next(res.results).text)
                speak(next(res.results).text)

            except StopIteration:
                speak("No se encontraron resultados")
        
        elif "parar de escuchar" in query:
            speak("Por cuantos segundos quieres que deje de escuchar tus comandos?")
            ans = int(TakeCommand())
            time.sleep(ans)
            print(ans)

        elif "cerrar sesión" in query:
            os.system("shutdown -l")

        elif "reiniciar" in query:
            os.system("shutdown /r /t 1")

        elif "apagar" in query:
            os.system("shutdown /s /t 1")