import sqlite3
from functions import getPlaylist
from constants import NEW_MUSIC_FRIDAY_ID
import datetime

def sqlConverter(id):
    # setup sqlite3
    db = sqlite3.connect("NewMusicFriday.db")
    c = db.cursor()

    # get week number and year
    date = datetime.datetime.now().isocalendar()
    week = date.week
    year = date.year

    sqlquery = "CREATE TABLE IF NOT EXISTS year{}week{}(id INTEGER, track TEXT, artists TEXT, loudness FLOAT, danceability FLOAT, valence FLOAT, instrumentalness FLOAT, speechiness FLOAT, acousticness FLOAT, key TEXT, duration INTEGER)".format(
        year, week
    )
    c.execute(sqlquery)

    # get the data
    data = getPlaylist(id)
    

    # insert the data
    insertquery = "INSERT INTO year{}week{}(id, track, artists, loudness, danceability, valence, instrumentalness, speechiness, acousticness, key, duration) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(
        year, week
    )
    for song in data["tracks"]:
        artistsDicts = data['tracks'][song]["artists"]
        a = []
        for artist in artistsDicts:
            a += artist
            
        c.execute(
            insertquery,
            (
                song,
                data['tracks'][song]["track"],
                ", ".join(a),
                data['tracks'][song]["audio_features"]["loudness"],
                data['tracks'][song]["audio_features"]["danceability"],
                data['tracks'][song]["audio_features"]["valence"],
                data['tracks'][song]["audio_features"]["instrumentalness"],
                data['tracks'][song]["audio_features"]["speechiness"],
                data['tracks'][song]["audio_features"]["acousticness"],
                data['tracks'][song]["audio_features"]["key"],
                data['tracks'][song]["audio_features"]["duration"],
            ),
        )


    db.commit()


# code for pythonanywhere tasks
day = datetime.datetime.today().weekday()
if day == 4:
    sqlConverter(NEW_MUSIC_FRIDAY_ID)