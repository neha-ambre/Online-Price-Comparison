import speech_recognition as sr

def speechToText():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Say something")
        audio=r.listen(source)
        
        try:
            print("You said: "+r.recognize_google(audio))
            return r.recognize_google(audio)
        except Exception as e:
            print("Error")
            return ""
            