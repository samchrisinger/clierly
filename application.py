from flask import *
from parser import parse
import json

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template('index.html', css=css,images=images,scripts=scripts)

@app.route('/parser',methods=['POST'])
def process():
    text = parse(request.form['text'])
    def map_text(p):
        return [{'text':sentence[0],'keywords':list(sentence[1]),'categories':list(sentence[2])} for sentence in p]
    text = map(map_text, text)
    return json.dumps(text)


if __name__ == '__main__':
    app.run('0.0.0.0')
