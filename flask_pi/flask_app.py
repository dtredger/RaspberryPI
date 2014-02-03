from flask import Flask, render_template
import datetime
import os

app = Flask(__name__)

@app.route("/")
def hello():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title': 'PiTools',
        'time': timeString
        }
    return render_template('main.html', **templateData)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('SERVER_PORT', 8080), debug=True)