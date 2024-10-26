from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('resume'))

@app.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме Івана Струтинського')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
