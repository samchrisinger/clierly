from flask import Flask, render_template, request
import json
import sys
from importlib import import_module

import settings as app_settings
# Load parser
parser = import_module('NLP.parsers.'+app_settings.PARSER+'.parser')

app = Flask(__name__)
app.config['DEBUG'] = True

def map_text(paragraph):
    return [{'text':sentence[0],'categories':list(sentence[1]),'message':sentence[2]} for sentence in paragraph]


@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/map')
def map():
    return render_template('map.html') 

@app.route('/demo')
def demo():
    return render_template('demo.html')
        
@app.route('/parser', methods=['POST'])
def process():
    text = parser.parse(request.form['text'])
    text = {'score': text[0], 'text': map(map_text, text[1])}
    return json.dumps(text)


if __name__ == '__main__':
    app.run('0.0.0.0')
