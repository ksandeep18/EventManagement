DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS attendees;

CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date TEXT NOT NULL,
    description TEXT
);

CREATE TABLE attendees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events (id)
);
