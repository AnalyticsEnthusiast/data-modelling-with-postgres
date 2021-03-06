import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Description: Reads in a single song file based on the filepath, then inserts
    the data into the target table using the cursor object. Loads song and artist
    data only.
    
    Arguments: 
        cur - Cursor object
        filepath - Path to input json file
    
    Returns: 
        None
    """
    # open song file
    df = pd.read_json(filepath, typ='series')

    # insert song record
    song_data = list(df[["song_id","title","artist_id","year","duration"]].values)
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = list(df[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].values)
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Description: Reads in a single log file based on the filepath, then inserts
    the data into the target table using the cursor object. Loads time, user and
    song_play data.
    
    Arguments: 
        cur - Cursor object
        filepath - Path to input json file
    
    Returns: 
        None
    """
    print(filepath)
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[(df['page'] == "NextSong")]

    # convert timestamp column to datetime
    df["ts"] = pd.to_datetime(df["ts"])
    
    # insert time data records
    time_data = (df["ts"], df["ts"].dt.hour, df["ts"].dt.day, df["ts"].dt.week, df["ts"].dt.month, df["ts"].dt.year, df["ts"].dt.weekday)
    column_labels = ("start_time", "hour", "day", "week", "month", "year", "weekday")
    z = zip(column_labels, time_data)
    t = dict(z)
    time_df = pd.DataFrame(t)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId","firstName","lastName","gender","level"]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, [row.song, row.artist, row.length])
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
            print(songid, " : ",artistid)
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, int(row.userId), row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Description: Executes either process_log_file or process_song_file
    for each file in the data/song_data or data/log_data directory.
    
    Arguments: 
        cur - Cursor object
        conn - Connection object
        filepath - Path to input directory
        func - Either process_log_file or process_song_file
    
    Returns: 
        None (Prints output to console)
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Description: Main executing loop. Sets up connection, cursor then
    processes the input files for logs and songs.
    
    Arguments: 
        None
    
    Returns: 
        None
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()