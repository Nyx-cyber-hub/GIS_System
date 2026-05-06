CREATE TABLE incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    severity TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);