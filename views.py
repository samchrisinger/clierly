from flask import render_template
from NLP import parser

def index(request):
    return render_template('index.html')

def process(request):
    text = parser.parse(request.form['text'])
    def map_text(p):
        return [{'text':sentence[0],'categories':list(sentence[1]),'message':sentence[2]} for sentence in p]
    text = map(map_text, text)
    # TODO render a template here
    return json.dumps(text)

