# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
#import sqlite3
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
import pyttsx3 
import speech_recognition as sr 
import datetime
import wikipedia
import webbrowser
#import os
#import smtplib
import sys
#import random
#from googlesearch import search 

#conn = sqlite3.connect('app.db')
#c = conn.cursor() 
#c.execute('CREATE TABLE IF NOT EXISTS  profile(username char(100) primary key ,age int,gender char(1),password varchar(14),sec_ans varchar(100))')


s= SoundLoader.load("song4.mp3")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def spk(audio):
        engine.say(audio)
        engine.runAndWait()
        
def wishMe():
        hour = int(datetime.datetime.now().hour)
        if hour>=0 and hour<12:
            spk("Good Morning!")
        elif hour>=12 and hour<16:
            spk("Good Afternoon!")
        else:
            spk("Good Evening!") 

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.5
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
    except Exception:
        query= "Say that again please..."
    return query
            
class MainWindow(Screen):
    pass

class SecondWindow(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs) 
    
    def validate_field1(self):
        
        acheck=self.ids.age
        gcheck=self.ids.gen
        
        aage=acheck.text
        ggen=gcheck.text
        info=self.ids.info
        
        if aage=='':
            info.text='Enter your age'
        elif int(aage)<8 :
            info.text = 'Sorry, you are too young.'
        elif ggen!='M' and ggen!='F' and ggen!='O':
            info.text='Invalid gender'
        elif ggen=='M' or ggen=='F' or ggen=='O' and int(aage)>8:
            self.manager.current="passwd"
            #c.execute(" update profile1 set aage=? , ggen=? ", (aage,ggen)) 
        
            
class ThirdWindow1(Screen): 
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
    
    def assignname(self):
        f=open(r"C:\Users\IAMWORLDLYWISE\APPLICATION1\randomnames.txt")
        username=self.ids.names
        for name in f.readlines():
            name=name.strip('\n')
            username.text=name
            #c.execute("update profile set username=? ", (name,))
            break

class ThirdWindow2(Screen):
    pass

class FourthWindow(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs) 
    
    def validate_pass(self):
        password=self.ids.passwd.text
        pswd2=self.ids.re_passwd.text
        sec_ans=self.ids.sec_answer.text
        info2=self.ids.info2
        
        if password==pswd2 and pswd2!='' and sec_ans!='' :
            self.manager.current="submit"
            #c.execute("update profile11 set password=? , sec_ans=? ", (pswd2,sec_ans))
        elif password!=pswd2:
            info2.text="Passwords do not match"
        elif password=='':
            info2.text="Create password"
        elif sec_ans=='':
            info2.text="Enter security answer"

class FourthWindow2(Screen):
    pass
            
class Home(Screen):
    pass
         
        

class Chat(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs) 
        
    def on_enter(self):
        Clock.schedule_once(self.start)
    
    def start(self,dt):
        wishMe()
        spk("I am    TETRA.")
        spk("Please tell me  how may I help you.")  
        
    def speak(self):
        qry=self.ids.qry
        qry.text="Listening..."
        rep=self.ids.rep
        rep.text=""
        Clock.schedule_once(self.mic)
        
    def ret_home(self):
        qry=self.ids.qry
        qry.text=""
        rep=self.ids.rep
        rep.text=""
        self.manager.current="home"
        
    def mic(self,dt):
        rep=self.ids.rep
        qry=self.ids.qry
        query = takeCommand().lower()
        qry.text= query
        fqry=open(r'C:\Users\IAMWORLDLYWISE\APPLICATION1\query.txt')
        if "ask me" in query:
            query=query.replace("ask me","")
            query=query.replace("i","you")
            spk(query)
            rep.text=query
        else:
            for line in fqry.readlines():
                fquery=line.split(':')[0]
                freply=line.split(':')[1]
                if fquery in query:
                    spk(freply)
                    rep.text=freply
                if 'wikipedia' in query:
                    spk('Searching Wikipedia...')
                    query = query.replace("wikipedia", "")
                    srch = wikipedia.summary(query, sentences=2)
                    rep.text="Definition from Wikipedia"
                    spk("According to Wikipedia")
                    spk(srch)
                    break
                elif query=='what is the time' or query=='tell me the time' or "what is the time" in query:
                    Time = datetime.datetime.now().strftime("%H:%M:%S")    
                    spk(f"The time is {Time}" )
                    rep.text= Time 
                    break
                elif query=="ok" or query=="okay" or query=="thankyou" or query=="thanks":
                    spk("thanks for trusting me")
                    rep.text="thanks for trusting me"
                    break
                elif 'open youtube' in query:
                    webbrowser.open("youtube.com")
                    spk("opening youtube")
                    break
                elif 'open google' in query:
                    webbrowser.open("google.com")
                    spk("opening google")
                    break
                elif 'am sad' in query:
                    s.play()
                    if "stop" or "pause" in query:
                        s.stop()
                elif query=="bye" or query=="exit" or query=="quit" or query=="bye-bye" or "bye" in query:
                    rep.text="see you soon"
                    spk("see you soon")
                    sys.exit()
                    break
                elif query=="shut up" or query=="get lost" or query=="you just get lost" or query=="you just shut up":
                    rep.text="sorry to hear this from you see you soon"
                    spk("i am sorry to hear this from you see you soon")
                    sys.exit()
                    break
    
    def reply(self):
        rep=self.ids.rep
        qry=self.ids.qry
        query1=self.ids.query1
        query=query1.text.lower()
        qry.text= query
        query1.text=''
        fqry=open(r'C:\Users\IAMWORLDLYWISE\APPLICATION1\query.txt')
        if "ask me" in query:
            query=query.replace("ask me","")
            query=query.replace("i","you")
            spk(query)
            rep.text=query
        else:
            for line in fqry.readlines():
                fquery=line.split(':')[0]
                freply=line.split(':')[1]
                if fquery in query:
                    spk(freply)
                    rep.text=freply
                if 'wikipedia' in query:
                    spk('Searching Wikipedia...')
                    query = query.replace("wikipedia", "")
                    srch = wikipedia.summary(query, sentences=2)
                    rep.text="Definition from Wikipedia"
                    spk("According to Wikipedia")
                    spk(srch)
                    break
                elif query=='what is the time' or query=='tell me the time' or "what is the time" in query:
                    Time = datetime.datetime.now().strftime("%H:%M:%S")    
                    spk(f"The time is {Time}" )
                    rep.text= Time 
                    break
                elif query=="ok" or query=="okay" or query=="thankyou" or query=="thanks":
                    spk("thanks for trusting me")
                    rep.text="thanks for trusting me"
                    break
                elif 'open youtube' in query:
                    webbrowser.open("youtube.com")
                    spk("opening youtube")
                    break
                elif 'open google' in query:
                    webbrowser.open("google.com")
                    spk("opening google")
                    break
                elif 'am sad' in query:
                    s.play()
                    if "stop" or "pause" in query:
                        s.stop()
                elif query=="bye" or query=="exit" or query=="quit" or query=="bye-bye" or "bye" in query:
                    rep.text="see you soon"
                    spk("see you soon")
                    sys.exit()
                    break
                elif query=="shut up" or query=="get lost" or query=="you just get lost" or query=="you just shut up":
                    rep.text="sorry to hear this from you see you soon"
                    spk("i am sorry to hear this from you see you soon")
                    sys.exit()
                    break
                    
class ProfileWindow(Screen):
    pass

class SettingWindow(Screen):
    pass

class HelpWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass
            
kv=Builder.load_file("widgets.kv")

class AURA(App):
    def build(self):
        return kv
        
if __name__ == '__main__':
    AURA().run()