# Sentimental 0.1

#### Description:
Sentimental 0.1 is an application that takes texts as input and outputs valences (positivity levels) from -5 to 5 of the texts individually and of the batch on average. 
The backend of the application is handled by C script that runs words of every given text against the AFINN dataset and calculates average valence. 
Front end is handled by Flask application.
SQLite3 database stores analysis history.

This project I intended as a foundation for my future more elaborate sentiment analysis efforts. Using it as a part of a financial trading algorithm, though ambitious, is also appealing to me.
I chose to implement C backend to get efficiency value out of it when using the application on large amounts of data. Input method would have to evolve for that, however. 
In its current form its just a basic proof of concept.

If the contents of this file are insufficient to understand certain details of the project, please, examine the files themselves. The commentary in some of them is extensive.

OpenAI's ChatGPT 4 and 4o were used in limited fashion as advisors and as an alternative to web search.

#### backend.c
Python part of the application calls backend.c using subprocess library. Input to the script is handled as text.

- In the main function correct amount of args is verified. 
- Afinn.csv is opened for reading
- Hash table is created. 
- nullifier function is used to set all of its buckets to NULL.
- The script uses table_filler function to load AFINN (which is a dataset manually created my Finn Årup Nielsen in 2009-2011 and is available for use copyright free.) into the hashtable of linked lists with nodes being data structs with words and their corresponding valences. The function also allocated memory for each node using malloc. 
- Polynomial Accummulation is used in the hash function for the table. Hash table was chosen to maximize the search speed.
- The main function calls valence-analyzer, the function that loops through input texts, uses strtok() to break them into words which it then compares to AFINN, gets valences and calculates their average. A specially edited string (with semi colons and new line chars to distinguish data points) is returned to python part.
- memory_cleaner function frees the allocated for AFINN memory recursively.
- Opened file is closed.
- All exceptions are coded to be sent up to Python using fprintf(stderr, "Error description here")

#### app.py
Main script of Flask in inside app.py. Has three routes: /, /history, /details. Plus apology function for rendering errors (similar to cs50 finance).

- / GET simply renders the main page (that has input fields).
- /history GET route calls sqlSelector function and uses its output to render history.html with the received data as a table
- /history POST route received input data (list of texts and topic as string), hands it to callC function, output of which is hands to sqlInserter. Then redirect is performed to the GET route.
- /details POST is responsible for displaying details of a batch that user chose from history table.
- apology function handles all errors (hopefully) via elaborate system of exceptions codded from bottom up in C script and other files. It renders apology.html with number and description of error.

app.py has a number of functions abstracted away into helpers.py

#### helpers.py
Is a separate file that has a set of functions abstracted away from app.py for better readability and clarity. sqlite3 library is used to query SQLite database.

- callC function calls the C script using subprocess library, gives it the set of texts for analysis, receives output string, breaks it into data points using predetermined seams (see backend.c), stores them in a list of tuples and returns it to app.py for further handling.
- sqlInserter function inserts its input data into SQL database.
- sqlSelector function fetches data from SQL database and returns it as a list of tuples
- sqlDetailedSelector takes id integer as an input and fetches data detailing every text of the batch with the said id from SQL database.
retrieved.

#### history.db
SQLite3 database has 2 tables: batches and texts.

- batches stores general information about each batch.
- texts has information about each individual text. References batch id's from the table 'batches'.

Schema:

```
CREATE TABLE batches(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    topic TEXT NOT NULL,
    size INTEGER NOT NULL,
    datetime TEXT NOT NULL
);
CREATE TABLE texts(
    local_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    batch_id INTEGER NOT NULL,
    valence REAL NOT NULL,
    analyzed_words INTEGER NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (batch_id)
    REFERENCES batches(id)
);
```

#### templates and static

- styles.css is the only static file. It has a few lines that prettify the tables (taken from CS50 finance). The rest of styling is handled by bootstrap.
- layout.html is the main template from which the other ones extend using jinja. Navbar from bootstrap is added here. It simply allows to navigate between main and history pages.
- index.html has input fields for texts and batch name, button for submission and button for adding new text fields (functionality implemented through javascript and DOM). Input data is handled via POST method to history route on submission.
- history.html loops through the list of tuples provided by app.py via jinja, renders its data as a table. It displays general data about each analyzed batch. Each entry has a button that leads to batch /details via POST method. 
- details.html loops through the list of tuples provided by app.py via jinja and renders as a table.
- apology.html renders error number and description of the specific error provided by app.py through jinja.
