from flask import Flask, render_template

app = Flask(__name__)

@app.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме Івана Струтинського')

if __name__ == '__main__':
    app.run(debug=True)
