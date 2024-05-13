from flask import Flask, render_template, request
import helpers

app = Flask(__name__)

@app.route('/')
def index():
    # Simply return the main page for input
    return render_template('layout.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Get text input from the form, the html page needs to send variable here
    # and it needs to call /analyze
    text = request.form['text']

    # implement call to C script which would do the actual analysis.
    # the call needs to pass the text there

    return render_template('output.html', output=output)
    # sentiment_result will be some kind of dictionary, perhaps a custom data struct
