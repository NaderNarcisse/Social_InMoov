#!/usr/bin/env python3
# Requires PyAudio and PySpeech and sounddevice.
 
import speech_recognition as sr
from time import ctime
import time
import os
import sys
import urllib.request
import urllib.parse
import re
from gtts import gTTS
from chatterbot  import ChatBot
import sounddevice as sd
from scipy.io.wavfile import write
import pygame
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

import webbrowser


#from googletrans import Translator
pygame.init()
r = sr.Recognizer()
#translator = Translator()

#chatbot setings
chatterbot = ChatBot('Leo')
trainer2 = ListTrainer(chatterbot)     #set the trainer
trainer1 = ChatterBotCorpusTrainer(chatterbot)

#training data
conversation = open('Data/chats.txt','r').readlines()
correction = open('Data/correction.txt','r').readlines()
correct = ""
message =""
archive = ""
chatting = True
def Train(): #pour train avec le corpus de base, puis un corpus perso, puis le corpus de correction
	speak("Because I'm cool, I'm gonna play some music while you are waiting")
	music = pygame.mixer.Sound("Data/Crockett's Theme (Chillwave Cover).wav")
	music.play()
	speak("i'm starting to train myself with stock data")
	trainer1.train("chatterbot.corpus.english")
	speak("I continue to train myself with standart conversation")
	trainer2.train(conversation) 
	speak("I'm now training with the correction text file")
	trainer2.train(correction)
	speak("training finished")
	music.fadeout(1500)

def speak(audioString): #pour parler ,+ traduire en fr si on veux,
    #translated = translator.translate(audioString, dest='fr')
    #audioString = translated.text
    audioString = str(audioString)
    print(audioString)
    tts = gTTS(text=audioString, lang='en-uk')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")
 
def recordAudio(): #cette fonction ne marchait pas probablement a cause de mon mic
    # Record Audio
    duration = 10.5  # seconds
    audio = sd.rec(int(duration * 48000), samplerate=48000, channels=1)
    sd.wait()
    write('output.wav', 48000, audio)
    
    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
 
    return data
 
def Liam(data): 
	if "hey" in data: #le 'hey' permet de déclencher une commande prédéfinie (pas en mode chatbot)
		if "how are you" in data:
			speak("I am fine")
 
		if "what time is it" in data:
			speak(ctime())
 
		if "where is" in data: #probablement inutile dans notre cas
			data = data.split(" ")
			location = data[2]
			speak("Hold on Gauthier, I will show you where " + location + " is.")
			webbrowser.open("https://www.google.nl/maps/place/" + location + "/&amp;")
			
			
		if "play me" in data: #si on veux faire chanter Leo
			data = data.split("play me")
			video = data[1]
			query_string = urllib.parse.urlencode({"search_query" : video})
			html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
			search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
			speak("ok, I will search for you the following video: " + video)
			print("http://www.youtube.com/watch?v=" + search_results[0])
			webbrowser.open("http://www.youtube.com/watch?v=" + search_results[0])

		
		if "record the good answer" in data: #pour enregistrer la bonne réponse (la fonction récup la question précédente, enregistre la réponse et enregistre le tout dans la fichier correction)
			speak("Ok, what is the answer?")
			correct = input("answer:")
			corrected = str("     :") + str(correct) + str("\n")
			print ("correct answer: ",corrected)
			reply = str(corrected)
			lines_of_text = [archive1, str(corrected)]
			acorrection = open('Data/correction.txt','a')
			acorrection.writelines(lines_of_text)
			acorrection.close()
			
		if "let's train" in data: #pour déclencher le train en pleine session
			conversation.close()
			correction.close()
			conversation = open('Data/chats.txt','r').readlines()
			correction = open('Data/correction.txt','r').readlines()
			Train()

	else : #réponses de base (sans 'hey')
		message = data
		if message.strip()!= 'Bye':
		    reply = chatterbot.get_response(message)
			print('Liam:',reply)
			speak(reply)
		if message.strip()=='Bye':
		    speak("Bye!")
		    chatting = False
		   
 
# initialization
time.sleep(2)
speak("Hi, I'm LEO. First of all, do you want me to train?")
Train_test = ""
while Train_test == "": #demande si train au début
	Train_test = input("Do you want to train? [y/n]")
if "y" in Train_test:
	Train()
else:
	speak("ok, no training today; let's chat!")
#main program
while chatting:
    #data = recordAudio()
    data = input("votre texte: ")
    archive1 = archive
    archive = str(data) + str("\n")
    print("archive=",archive1)
    Liam(data)
