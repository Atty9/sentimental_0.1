from flask import Flask, render_template, request, redirect
import helpers

app = Flask(__name__)


@app.after_request
def after_request(response):
    '''
    Ensures no cache saving
    '''
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/')
def index():
    '''
    Renders the main page (responsible for input)
    '''
    
    return render_template('index.html')


@app.route('/history', methods=['POST', 'GET'])
def history():
    '''
    On POST:
    Handles input from the main page
    Calls C script for sentiment analysis of the input
    Receives C script output
    Adds output data to SQL db
    Renders history of analysis history from SQL db
    On GET:
    Simply renders history from SQL db
    '''

    if request.method == 'POST':

        texts = request.form.getlist('texts')
        topic = request.form.get("topic")
        if not topic or not texts or not any(texts):
            return apology(400,"Topic and Text fields must not be empty")
        if len(topic) > 30:
            return apology(400,"Topic must be under 30 symbols")
        
        helpers.cleanser(texts)
        output = helpers.callC(texts)
        if isinstance(output, str):
            return apology(500,"Internal C Error: " + output)
        if len(output) != len(texts):
            return apology(500,"Internal Error: C script input/output discrepancy")

        tempOut = helpers.sqlInserter(texts, output, topic) 
        if tempOut != None:
            return apology(500,"Internal SQL Error: " + tempOut)

        return redirect('/history')

    else:

        selection = helpers.sqlSelector()
        if isinstance(selection, str):
            return apology(500,"Internal SQL Error: " + selection)
        if not selection or not any(selection):
            return apology(500,"Internal Error: Database request empty output")
        
        return render_template('history.html', theList=selection)


@app.route('/details', methods=['POST'])
def details():
    '''
    Renders details of a batch with with the input id
    '''

    id = request.form.get("id")
    if not id:
        return apology(500, "Internal Error: Failure retriving batch id")

    selection = helpers.sqlDetailedSelector(id)
    if isinstance(selection, str):
        return apology(500,"Internal SQL Error: " + selection)
    if not selection or not any(selection):
        return apology(500, "Internal Error: Database request empty output")

    return render_template('details.html', theList=selection, id=id)


def apology(error, message):
    '''
    Renders errors
    '''

    return render_template('apology.html', error=error, message=message)


if __name__ == '__main__':
    app.run(debug=True)