from flask import Flask, render_template

app = Flask(__name__)

@app.route('/resume')
def resume():
    return render_template('resume.html')
