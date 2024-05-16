from flask import Flask, render_template, request
import helpers

app = Flask(__name__)

# Verify input
# Plan and create SQL database for analysis history

@app.route('/', methods=['GET'])
def index():
    # renders the main page (responsible for input)
    return render_template('index.html')

@app.route('/output', methods=['POST'])
def output():
    '''
    Handles input from the main page, calls backend, renders output
    Adds data to SQL db
    '''

    texts = request.form.getlist('texts')
    output = helpers.callC(texts)
    
    helpers.sqlInserter(texts, output)

    return render_template('output.html', theDict=output)
    
if __name__ == '__main__':
    app.run(debug=True)