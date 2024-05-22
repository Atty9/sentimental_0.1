from flask import Flask, render_template, request
import helpers

app = Flask(__name__)

# Anything that could go wrong with incorrect input?
# Add error system like in finance
# redundancy between output and history backend (leave history only)

@app.route('/')
def index():
    '''
    Renders the main page (responsible for input)
    '''
    
    return render_template('index.html')

@app.route('/output', methods=['POST'])
def output():
    '''
    Handles input from the main page, calls backend, renders output
    Adds data to SQL db
    '''

    texts = request.form.getlist('texts')
    topic = request.form.get("topic") # check syntax, update index.html with topic input
    output = helpers.callC(texts)
    
    if len(output) != len(texts):
        return "Error: the texts"

    helpers.sqlInserter(texts, output, topic)

    return render_template('output.html', theList=output) # update output.html with all the SQL data

@app.route('/history')
def history():
    '''
    Renders history of analysis batches from sql db
    Calls /details on batch details request 
    '''

    selection = helpers.sqlSelector()
    return render_template('history.html', theList=selection)

@app.route('/details', methods=['POST'])
def details():
    '''
    Renders details of a batch with with the input id
    '''

    selection = helpers.sqlDetailedSelector(request.form.get("id"))
    return render_template('details.html', theList=selection)
    
if __name__ == '__main__':
    app.run(debug=True)