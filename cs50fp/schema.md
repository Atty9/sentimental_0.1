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