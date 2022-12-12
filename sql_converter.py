from auth import sp
from constants import trackKeyDict, topHitsPlaylists
import sqlite3


def getPlaylist(year):
    """Get all the relevant info from a "TopHits" playlist from a given year"""
    # request from spotipy
    playlist = sp.playlist(topHitsPlaylists[year])["tracks"]["items"]
    playlistLength = len(playlist)

    # empty dict for the final values
    playlistDict = {}

    # loop through each song in the playlist and get the wanted data
    for i in range(playlistLength):
        playlistDict[i + 1] = {}
        track = playlist[i]["track"]

        artists = track["artists"]
        trackArtists = []
        for j in range(len(artists)):
            trackArtists.append(artists[j]["name"])

        trackName = track["name"]
        trackId = track["id"]
        trackAudioFeatures = sp.audio_features(trackId)[0]
        try:
            trackLoudness = trackAudioFeatures["loudness"]
        except TypeError:
            trackLoudness = "n/a"

        try:
            trackDanceability = trackAudioFeatures["danceability"]
        except TypeError:
            trackDanceability = "n/a"

        try:
            trackValence = trackAudioFeatures["valence"]
        except TypeError:
            trackValence = "n/a"

        try:
            trackInstrumentalness = trackAudioFeatures["instrumentalness"]
        except TypeError:
            trackInstrumentalness = "n/a"

        try:
            trackSpeechiness = trackAudioFeatures["speechiness"]
        except TypeError:
            trackSpeechiness = "n/a"

        try:
            trackAcousticness = trackAudioFeatures["acousticness"]
        except TypeError:
            trackAcousticness = "n/a"

        try:
            trackKey = trackAudioFeatures["key"]
            trackMode = ""

            if trackKey >= 0:
                trackMode = trackAudioFeatures["mode"]
                if trackMode == 1:
                    trackMode = "Major"
                else:
                    trackMode = "Minor"

            trackKey = trackKeyDict[trackKey]
        except:
            trackKey = "n/a"
            trackMode = ""

        try:
            trackDuration = trackAudioFeatures["duration_ms"]
        except TypeError:
            trackDuration = "n/a"

        playlistDict[i + 1] = {
            "track": trackName,
            "artists": trackArtists,
            "loudness": trackLoudness,
            "danceability": trackDanceability,
            "valence": trackValence,
            "instrumentalness": trackInstrumentalness,
            "speechiness": trackSpeechiness,
            "acousticness": trackAcousticness,
            "key": trackKey + " " + trackMode,
            "duration": trackDuration,
        }

    return playlistDict


# setup sqlite3
db = sqlite3.connect("SpotifyTopHits.db")
c = db.cursor()

# create a table for each year
for year in topHitsPlaylists:
    sqlquery = "CREATE TABLE TopHits{}(id INTEGER, track TEXT, artists TEXT, loudness FLOAT, danceability FLOAT, valence FLOAT, instrumentalness FLOAT, speechiness FLOAT, acousticness FLOAT, key TEXT, duration INTEGER)".format(
        str(year)
    )
    c.execute(sqlquery)

    # get the data
    data = getPlaylist(year)

    # insert the data
    insertquery = "INSERT INTO TopHits{}(id, track, artists, loudness, danceability, valence, instrumentalness, speechiness, acousticness, key, duration) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(
        str(year)
    )
    for song in data:
        c.execute(
            insertquery,
            (
                song,
                data[song]["track"],
                ", ".join(data[song]["artists"]),
                data[song]["loudness"],
                data[song]["danceability"],
                data[song]["valence"],
                data[song]["instrumentalness"],
                data[song]["speechiness"],
                data[song]["acousticness"],
                data[song]["key"],
                data[song]["duration"],
            ),
        )

    print(year)


db.commit()
