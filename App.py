from flask import Flask, render_template, flash, request, url_for
import numpy as np
import pandas as pd
import re
import os
import tensorflow as tf
from numpy import array
from keras.datasets import imdb
from keras.preprocessing import sequence
from keras.models import load_model

IMAGE_FOLDER = os.path.join('static','img_pool')

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

def init():
    global model, graph
    #Loading Of LSTM Model File In Single Quotes...
    model = load_model('Sentimental_Analysis.ipynb')
    graph = tf.get_default_graph()

@app.route('/',methods=['GET','POST'])
@app.route("/")
@app.route("/home")
def home():
    title = "Home Page"
    return render_template('Home.html',title=title)

@app.route('/sentiment_analysis_prediction',methods = ['POST',"GET"])
def sent_anly_prediction():
    if request.method == 'POST':
        text = request.form['text']
        Sentiment = " "
        max_review_length = 500
        word_to_id = imdb.get_word_index()
        strip_special_chars = re.complex("[^A-Za-z0-9 ]+")
        text = text.lower().replace("<br />"," ")
        text = re.sub(strip_special_chars,"",text.lower())

        words = text.split()
        x_test = [[word_to_id[word] if (word in word_to_id and word_to_id[word]<=20000) else 0 for word in words]]
        x_test = sequence.pad_sequences(x_test,maxlen=500)
        vector = np.array([x_test.flatten()])
        with graph.as_default():
            probability = model.predict(array([vector][0]))[0][0]
            class1 = model.predict_classes(array([vector][0]))[0][0]
        if class1 == 0:
            sentiment = "Negative"
            img_filename = os.path.join(app.config['UPLOAD_FOLDER'],'Sad.png')
        else:
            sentiment = "Positive"
            img_filename = os.path.join(app.config['UPLOAD_FOLDER'],'Smile.png')
    return render_template('home.html',text=text,sentiment=sentiment, probability=probability, image=img_filename)

if __name__ == '__main__':
    init()
    (app.run(debug=True))