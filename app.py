from flask import Flask, render_template, render_template_string

app = Flask(__name__)

@app.route('/hello')
def hello():
    return render_template_string('<h1>Hello</h1>') 
