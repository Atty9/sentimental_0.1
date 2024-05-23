from flask import Flask, render_template, request
import helpers

app = Flask(__name__)


# Add functionality to history to request details
# Warn, truncate the topic to managable lenth
# Add error system like in finance

@app.route('/') # Add topic input on top
def index():
    '''
    Renders the main page (responsible for input)
    '''
    
    return render_template('index.html')

@app.route('/history', methods=['POST'])
def output():
    '''
    Handles input from the main page
    Calls C script for sentiment analysis
    Adds C output to SQL db
    Renders history of all analyses
    '''

    texts = request.form.getlist('texts')
    topic = request.form.get("topic") # check syntax, update index.html with topic input
    output = helpers.callC(texts)
    
    if len(output) != len(texts):
        return "Error: inconsistency in the number of texts in and out of C script"

    helpers.sqlInserter(texts, output, topic)
    selection = helpers.sqlSelector() 

    return render_template('history.html', theList=selection)

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