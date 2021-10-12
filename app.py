import pyaudio
import speech_recognition as sr
from nltk import NaiveBayesClassifier as nbc
from pythainlp.tokenize import word_tokenize
import codecs
from itertools import chain
import pandas as pd
import json
from flask import Flask,request,jsonify
import numpy as np

#############################################################################################
################################  SENTIMENT SETUP  ##########################################

# pos.txt
with codecs.open('pos.txt', 'r', "utf-8") as f:
    lines = f.readlines()
listpos=[e.strip() for e in lines]
del lines
f.close() 

# neg.txt
with codecs.open('neg.txt', 'r', "utf-8") as f:
    lines = f.readlines()
listneg=[e.strip() for e in lines]
f.close() 

# neutral.txt
with codecs.open('neutral.txt', 'r', "utf-8") as f:
    lines = f.readlines()
listneu=[e.strip() for e in lines]
f.close() 

pos1=['positive']*len(listpos)
neg1=['negative']*len(listneg)
neu1=['neutral']*len(listneu)

training_data = list(zip(listpos,pos1)) + list(zip(listneg,neg1)) + list(zip(listneg,neu1))
vocabulary = set(chain(*[word_tokenize(i[0].lower()) for i in training_data]))
feature_set = [({i:(i in word_tokenize(sentence.lower())) for i in vocabulary},tag) for sentence, tag in training_data]
classifier = nbc.train(feature_set)

#############################################################################################

def sentiment(sentence):
    text = []
    test_sentence = sentence
    featurized_test_sentence =  {i:(i in word_tokenize(test_sentence.lower())) for i in vocabulary} 
    sentiment = classifier.classify(featurized_test_sentence)
    my_array = np.array([test_sentence, sentiment])
    text.append(my_array)
    df = pd.DataFrame(text, columns = ['text','sentiment'])
    result = df.to_json(orient="index")
    parsed = json.loads(result)
    return parsed

#############################################################################################
################################  MIC SETUP  ##########################################

sr.Microphone.list_microphone_names()

mic = sr.Microphone(1)
recog = sr.Recognizer()


with mic as source:
 audio = recog.listen(source)
 word = recog.recognize_google(audio,language='th')

# data =[]
# with mic as source:
#     while True:
#         audio = recog.listen(source)
#         try:
#             data.append(recog.recognize_google(audio,language='th'))
#             print(recog.recognize_google(audio,language='th'))
#         except:
#             continue

# def sentiment_analyst(data_test):
#     test = []
#     for i in data_test:
#         test.append(sentiment(i))
#     df = pd.DataFrame(test, columns = ['text','sentiment'])
#     result = df.to_json(orient="records")
#     parsed = json.loads(result)
#     return parsed

sentiment(word)
