# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS song_play_fact;"
user_table_drop = "DROP TABLE IF EXISTS user_dim;"
song_table_drop = "DROP TABLE IF EXISTS song_dim;"
artist_table_drop = "DROP TABLE IF EXISTS artist_dim;"
time_table_drop = "DROP TABLE IF EXISTS time_dim;"


# CREATE TABLES
user_table_create = ("""
    CREATE TABLE IF NOT EXISTS user_dim (
        user_id int PRIMARY KEY,
        first_name varchar(100),
        last_name varchar(100),
        gender varchar(1),
        level varchar(5)
    );
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS song_dim (
        song_id varchar(100) PRIMARY KEY, 
        title varchar(100),
        artist_id varchar(100),
        year int,
        duration decimal(8,5)
    );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artist_dim (
        artist_id varchar(100) PRIMARY KEY,
        name varchar(100),
        location varchar(200),
        latitude DECIMAL(10,8), 
        longitude DECIMAL(11,8)
    );
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time_dim (
        start_time timestamp PRIMARY KEY, 
        hour int, 
        day int, 
        week int, 
        month int, 
        year int, 
        weekday int
    );
""")


songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS song_play_fact (
        songplay_id serial PRIMARY KEY,
        start_time timestamp REFERENCES time_dim (start_time),
        user_id int REFERENCES user_dim (user_id),
        level varchar(5),
        song_id varchar(100) REFERENCES song_dim (song_id),
        artist_id varchar(100) REFERENCES artist_dim (artist_id), 
        session_id int,
        location varchar(200),
        user_agent varchar(255)
    );
""")


# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO song_play_fact ( 
    start_time, 
    user_id,  
    level, 
    song_id, 
    artist_id,  
    session_id,
    location, 
    user_agent
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (songplay_id) DO NOTHING
""")

user_table_insert = ("""
    INSERT INTO user_dim (
    user_id,
    first_name,
    last_name,
    gender,
    level
    )
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id)
    DO UPDATE SET level = EXCLUDED.level;
""")

song_table_insert = ("""
    INSERT INTO song_dim (
    song_id, 
    title, 
    artist_id, 
    year, 
    duration
    )
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (song_id) DO NOTHING;
    """)

artist_table_insert = ("""
    INSERT INTO artist_dim (
    artist_id,
    name,
    location,
    latitude, 
    longitude
    )
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id) DO NOTHING;
""")

time_table_insert = ("""
    INSERT INTO time_dim (
    start_time, 
    hour, 
    day, 
    week, 
    month, 
    year, 
    weekday
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (start_time) DO NOTHING;
""")

# FIND SONGS
#  where -> title, artist name, and duration
# Fields -> timestamp, user ID, level, song ID, artist ID, session ID, location, and user agent 
#  --AND s.duration = %s
song_select = ("""
    SELECT
        s.song_id,
        a.artist_id
    FROM song_dim s
    JOIN artist_dim a
    ON s.artist_id = a.artist_id
    WHERE s.title = %s
    AND a.name = %s
    AND s.duration = %s
""")

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]