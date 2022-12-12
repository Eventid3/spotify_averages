from auth import sp
from constants import trackKeyDict, topHitsPlaylists
from flask import Flask


# old function - not currently used
def getAvarage(dataType, dict, length):
    """Get the average value of a given data from a certain year"""
    
    dataTotal = 0

    for i in range(length):
        
        errorFix = 0
        try:
            dataTotal += dict[i+1]["audio_features"][dataType]
        except TypeError:
            errorFix -= 1
            continue

    if dataType == "loudness":
        return round((dataTotal / (length - errorFix)), 3)
        
    return dataTotal / (length - errorFix)


def searchSpotify(query):
    results = sp.search(query, type="track,album,artist,playlist")
    resultDict = {}

    for result in results:
        resultDict[result] = {}

        for entry in results[result]["items"]:
            resultDict[result][entry["name"]] = {}
            resultDict[result][entry["name"]]["id"] = entry["id"]
            resultDict[result][entry["name"]]["url"] = entry["external_urls"]["spotify"]
            if result == "tracks":
                try:
                    resultDict[result][entry["name"]]["img"] = entry["album"]["images"][
                        0
                    ]["url"]
                except:
                    resultDict[result][entry["name"]][
                        "img"
                    ] = "/static/images/placeholder.png"

                resultDict[result][entry["name"]]["artists"] = []

                for artist in entry["artists"]:
                    resultDict[result][entry["name"]]["artists"].append(artist["name"])

            elif result == "artists":
                try:
                    resultDict[result][entry["name"]]["img"] = entry["images"][0]["url"]
                except:
                    resultDict[result][entry["name"]][
                        "img"
                    ] = "/static/images/artistplaceholder.png"

            else:
                if result == "albums":
                    resultDict[result][entry["name"]]["artists"] = []
                    for artist in entry["artists"]:
                        resultDict[result][entry["name"]]["artists"].append(
                            artist["name"]
                        )
                try:
                    resultDict[result][entry["name"]]["img"] = entry["images"][0]["url"]
                except:
                    resultDict[result][entry["name"]][
                        "img"
                    ] = "/static/images/placeholder.png"

    return resultDict


def getAudioFeatures(id):
    trackAudioFeatures = sp.audio_features(id)[0]

    audioFeaturesDict = {}

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
    except:
        trackDuration = None

    audioFeaturesDict = {
        "loudness": trackLoudness,
        "danceability": trackDanceability,
        "valence": trackValence,
        "instrumentalness": trackInstrumentalness,
        "speechiness": trackSpeechiness,
        "acousticness": trackAcousticness,
        "key": trackKey + " " + trackMode,
        "duration": trackDuration,
    }

    return audioFeaturesDict


def getArtists(artists):
    artistList = []

    try:
        artists = artists["artists"]
    except:
        return artistList

    for i in range(len(artists)):
        artistList.append({artists[i]["name"]: artists[i]["id"]})

    return artistList


def getAlbum(id):
    album = sp.album(id)
    albumLength = len(album["tracks"]["items"])

    albumDict = {}

    albumDict["type"] = "album"

    try:
        albumDict["img"] = album["images"][0]["url"]
    except:
        albumDict["img"] = "/static/images/placeholder.png"
    try:
        albumDict["name"] = album["name"]
    except:
        albumDict["name"] = ""

    albumDict["artists"] = getArtists(album)

    albumDict["tracks"] = {}

    for i in range(albumLength):
        albumDict["tracks"][i + 1] = {}
        try:
            trackName = album["tracks"]["items"][i]["name"]
        except:
            trackName = ""
        try:
            trackId = album["tracks"]["items"][i]["id"]
        except:
            trackId = ""

        albumDict["tracks"][i + 1] = {
            "track": trackName,
            "audio_features": getAudioFeatures(trackId),
        }
    
    albumDict["averages"] = {
        "loudness" : getAvarage("loudness", albumDict["tracks"], albumLength),
        "danceability" : getAvarage("danceability", albumDict["tracks"], albumLength),
        "valence" : getAvarage("valence", albumDict["tracks"], albumLength),
        "instrumentalness" : getAvarage("instrumentalness", albumDict["tracks"], albumLength),
        "speechiness" : getAvarage("speechiness", albumDict["tracks"], albumLength),
        "acousticness" : getAvarage("acousticness", albumDict["tracks"], albumLength),
        "duration" : getAvarage("duration", albumDict["tracks"], albumLength),
        }

    return albumDict


def getTrack(id):
    track = sp.track(id)
    trackDict = {}
    trackDict["tracks"] = {}
    trackDict["tracks"][1] = {}

    trackDict["type"] = "track"

    try:
        trackDict["img"] = track["album"]["images"][0]["url"]
    except:
        trackDict["img"] = "/static/images/placeholder.png"
    try:
        trackDict["name"] = track["name"]
    except:
        trackDict["name"] = ""
    try:
        trackDict["album"] = track["album"]["name"]
    except:
        trackDict["album"] = ""

    trackDict["artists"] = getArtists(track)

    trackDict["tracks"][1]["audio_features"] = getAudioFeatures(id)

    return trackDict


def getPlaylist(id):
    playlist = sp.playlist(id)
    playlistLength = len(playlist["tracks"]["items"])

    playlistDict = {}
    playlistDict["type"] = "playlist"
    try:
        playlistDict["name"] = playlist["name"]
    except:
        playlistDict["name"]
    try:
        playlistDict["img"] = playlist["images"][0]["url"]
    except:
        playlistDict["img"] = "/static/images/placeholder.png"

    playlistDict["tracks"] = {}

    for i in range(playlistLength):
        playlistDict["tracks"][i + 1] = {}

        track = playlist["tracks"]["items"][i]["track"]

        trackArtists = getArtists(track)

        try:
            trackName = track["name"]
        except:
            trackName = ""
        try:
            trackId = track["id"]
        except:
            trackId = ""

        playlistDict["tracks"][i + 1] = {
            "track": trackName,
            "artists": trackArtists,
            "audio_features": getAudioFeatures(trackId),
        }
    
    playlistDict["averages"] = {
        "loudness" : getAvarage("loudness", playlistDict["tracks"], playlistLength),
        "danceability" : getAvarage("danceability", playlistDict["tracks"], playlistLength),
        "valence" : getAvarage("valence", playlistDict["tracks"], playlistLength),
        "instrumentalness" : getAvarage("instrumentalness", playlistDict["tracks"], playlistLength),
        "speechiness" : getAvarage("speechiness", playlistDict["tracks"], playlistLength),
        "acousticness" : getAvarage("acousticness", playlistDict["tracks"], playlistLength),
        "duration" : getAvarage("duration", playlistDict["tracks"], playlistLength),
        }

    return playlistDict


def getArtistAlbums(id):
    albums = sp.artist_albums(id, limit=50)
    artist = sp.artist(id)
    albumsDict = {}
    albumsDict["type"] = "artist"
    albumsDict["artists"] = [{artist["name"]: artist["id"]}]
    try:
        albumsDict["img"] = artist["images"][0]["url"]
    except:
        albumsDict["img"] = "/static/images/artistplaceholder.png"
    albumsDict["albums"] = {}
    albumsDict["singles"] = {}
    albumsDict["compilations"] = {}

    for i in range(len(albums["items"])):
        if albums["items"][i]["album_type"] == "album":
            albumsDict["albums"][albums["items"][i]["name"]] = {}
            albumsDict["albums"][albums["items"][i]["name"]]["id"] = albums["items"][i][
                "id"
            ]
            albumsDict["albums"][albums["items"][i]["name"]]["release"] = albums[
                "items"
            ][i]["release_date"]
            try:
                albumsDict["albums"][albums["items"][i]["name"]]["img"] = albums[
                    "items"
                ][i]["images"][0]["url"]
            except:
                albumsDict["albums"][albums["items"][i]["name"]][
                    "img"
                ] = "/static/imgages/placeholder.png"
        if albums["items"][i]["album_type"] == "single":
            albumsDict["singles"][albums["items"][i]["name"]] = {}
            albumsDict["singles"][albums["items"][i]["name"]]["id"] = albums["items"][
                i
            ]["id"]
            albumsDict["singles"][albums["items"][i]["name"]]["release"] = albums[
                "items"
            ][i]["release_date"]
            try:
                albumsDict["singles"][albums["items"][i]["name"]]["img"] = albums[
                    "items"
                ][i]["images"][0]["url"]
            except:
                albumsDict["singles"][albums["items"][i]["name"]][
                    "img"
                ] = "/static/imgages/placeholder.png"
        if albums["items"][i]["album_type"] == "compilation":
            albumsDict["compilations"][albums["items"][i]["name"]] = {}
            albumsDict["compilations"][albums["items"][i]["name"]]["id"] = albums[
                "items"
            ][i]["id"]
            albumsDict["compilations"][albums["items"][i]["name"]]["release"] = albums[
                "items"
            ][i]["release_date"]
            try:
                albumsDict["compilations"][albums["items"][i]["name"]]["img"] = albums[
                    "items"
                ][i]["images"][0]["url"]
            except:
                albumsDict["compilations"][albums["items"][i]["name"]][
                    "img"
                ] = "/static/imgages/placeholder.png"

    print(albumsDict)
    return albumsDict


def percent(value):
    """Format value as percent."""
    try:
        return f"{(value*100):,.2f}%"
    except:
        return value


def time(value):
    """Format value as minutes and seconds."""
    try:
        minutes = int((value / 1000) / 60)
        seconds = (value / 1000) % 60
        return "%im%is" % (minutes, seconds)
    except:
        return value


def artists(value):
    try:
        return ", ".join(value)
    except:
        return value


def id(value):
    return str(value)


def capitalize(value):
    return value.replace('"', "").upper()


def releaseYear(value):
    return value[:4]
