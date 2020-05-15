from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from gtts import gTTS
import os
import speech_recognition as sr

chatbot = ChatBot('Leo')
mic = sr.Microphone()
r = sr.Recognizer()

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

def speak(tex):
	text = str(tex)
	print(text)
	tts = gTTS(text=text, lang='en-UK')
	tts.save("audio.mp3")
	os.system("mpg321 audio.mp3")
# Train the chatbot based on the english corpus
#trainer.train("chatterbot.corpus.english")


def response(msg):
	# Get a response to an input statement
	res = chatbot.get_response(msg)
	speak(res)

while True:
	with mic as source:
		r.adjust_for_ambient_noise(source, duration=0.2)
		audio = r.listen(source)
		msg = r.recognize_google(audio)
		print(msg)
		response(msg)
