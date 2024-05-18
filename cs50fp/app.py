from flask import Flask, render_template, request
import helpers

app = Flask(__name__)

# Anything that could go wrong with incorrect input?

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
    output = helpers.callC(texts)
    
    # helpers.sqlInserter(texts, output)

    return render_template('output.html', theList=output)

@app.route('/history')
def history():
    '''
    Renders history of analysis batches from sql db
    Calls /details on batch details request 
    '''

    selection = helpers.sqlSelector()
    return render_template('history.html', theDict=selection)

@app.route('/details', methods=['POST'])
def details():
    '''
    Render details of a batch of analysed text per input id
    '''

    selection = helpers.sqlDetailedSelector(request.form.get("id"))
    return render_template('details.html', theDict=selection)
    
if __name__ == '__main__':
    app.run(debug=True)