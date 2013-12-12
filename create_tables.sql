CREATE TABLE IF NOT EXISTS
    genres (genre_id INTEGER PRIMARY KEY,
            name TEXT,
            url TEXT NOT NULL,
            parent_id INTEGER,
            movie_count INTEGER,
            skipped BOOL);

CREATE TABLE IF NOT EXISTS
    movies (id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id TEXT,
            name TEXT NOT NULL,
            cover_url TEXT,
            movie_url TEXT,
            info TEXT,
            genres TEXT);
