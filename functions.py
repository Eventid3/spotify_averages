from auth import sp
from constants import trackKeyDict, topHitsPlaylists
from flask import Flask        

def getAvarage(data, year):
    '''Get the average value of a given data from a certain year'''
    playlist = sp.playlist(topHitsPlaylists[year])["tracks"]["items"]
    playlistLength = len(playlist)
    dataTotal = 0
    
    for i in range(playlistLength):
        trackId = playlist[i]["track"]["id"]
        trackAudioFeatures = sp.audio_features(trackId)[0]
        errorFix = 0
        try:
            dataTotal += trackAudioFeatures[data]
        except TypeError:
            errorFix -= 1
            continue
    
    return dataTotal / (playlistLength - errorFix)


def searchSpotify(query):
    results = sp.search(query, type="track,album,artist,playlist")
    resultDict = {}
    
    for result in results:
        resultDict[result] = {}
        
        for entry in results[result]['items']:
            resultDict[result][entry['name']] = {}
            resultDict[result][entry['name']]['id'] = entry['id']
            resultDict[result][entry['name']]['url'] = entry['external_urls']['spotify']
            if result == 'tracks':
                try:
                    resultDict[result][entry['name']]['img'] = entry['album']['images'][0]['url']
                except:
                    resultDict[result][entry['name']]['img'] = "/static/images/placeholder.png"
                    
                resultDict[result][entry['name']]['artists'] = []
                
                for artist in entry['artists']:
                    resultDict[result][entry['name']]['artists'].append(artist['name'])
                    
            elif result == 'artists':
                try:
                    resultDict[result][entry['name']]['img'] = entry['images'][0]['url']
                except:
                    resultDict[result][entry['name']]['img'] = "/static/images/artistplaceholder.png"
                    
            else:
                if result == 'albums':
                    resultDict[result][entry['name']]['artists'] = []
                    for artist in entry['artists']:
                        resultDict[result][entry['name']]['artists'].append(artist['name'])     
                try:
                    resultDict[result][entry['name']]['img'] = entry['images'][0]['url']
                except:
                    resultDict[result][entry['name']]['img'] = "/static/images/placeholder.png"
            
                    
    return resultDict


def getAlbum(id):
    album = sp.album(id)
    albumLength = len(album['tracks']['items'])

    albumDict = {}
    
    albumDict['type'] = "album"
    
    try:
        albumDict['img'] = album['images'][0]['url']
    except:
        albumDict['img'] = "/static/images/placeholder.png"
    try:
        albumDict['name'] = album['name']
    except:
        albumDict['name'] = ""
        
    artists = album["artists"]
    albumArtists = []
    for i in range(len(artists)):
        albumArtists.append(artists[i]["name"])
    albumDict['artists'] = albumArtists
    
    albumDict['tracks'] = {}

    for i in range(albumLength):
        albumDict['tracks'][i+1] = {}
        try:
            trackName = album['tracks']['items'][i]['name']
        except:
            trackName = ""
        try:
            trackId = album['tracks']['items'][i]['id']
        except:
            trackId = ""
        
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
        except:
            trackDuration = None
        
        albumDict['tracks'][i+1] = {
            "track": trackName, 
            "loudness" : trackLoudness,  
            "danceability" : trackDanceability, 
            "valence" : trackValence,
            "instrumentalness" : trackInstrumentalness,
            "speechiness" : trackSpeechiness,
            "acousticness" : trackAcousticness,
            "key" : trackKey + " " + trackMode,
            "duration" : trackDuration
            }
        
    return albumDict


def getTrack(id):
    track = sp.track(id)
    trackDict = {}
    trackDict['tracks'] = {}
    trackDict['tracks'][1] = {}
    
    trackDict['type'] = "track"
    
    try:
        trackDict['img'] = track['album']['images'][0]['url']
    except:
        trackDict['img'] = "/static/images/placeholder.png"
    try:
        trackDict['name'] = track['name']
    except:
        trackDict['name'] = ""
    try:
        trackDict['album'] = track['album']['name']
    except:
        trackDict['album'] = ""
    
    try:
        artists = track["artists"]
    except:
        artists = ""
    trackArtists = []
    for i in range(len(artists)):
        trackArtists.append(artists[i]["name"])
        
    trackDict['artists'] = trackArtists
    
    trackAudioFeatures = sp.audio_features(id)[0]
    
    try:
        trackDict['tracks'][1]["loudness"] = trackAudioFeatures["loudness"]
    except TypeError:
        trackDict['tracks'][1]["loudness"] = "n/a"
        
    try:
        trackDict['tracks'][1]["danceability"] = trackAudioFeatures["danceability"]
    except TypeError:
        trackDict['tracks'][1]["danceability"] = "n/a"
        
    try:
        trackDict['tracks'][1]["valence"] = trackAudioFeatures["valence"]
    except TypeError:
        trackDict['tracks'][1]["valence"] = "n/a"               
    
    try:
        trackDict['tracks'][1]["instrumentalness"] = trackAudioFeatures["instrumentalness"]
    except TypeError:
        trackDict['tracks'][1]["instrumentalness"] = "n/a"        

    try:
        trackDict['tracks'][1]["speechiness"] = trackAudioFeatures["speechiness"]
    except TypeError:
        trackDict['tracks'][1]["speechiness"] = "n/a"         
    
    try:
        trackDict['tracks'][1]["acousticness"] = trackAudioFeatures["acousticness"]
    except TypeError:
        trackDict['tracks'][1]["acousticness"] = "n/a"           
    
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
    
    trackDict['tracks'][1]["key"] = trackKey + " " + trackMode
        
    trackDict['tracks'][1]["duration"] = trackAudioFeatures["duration_ms"]
    
    return trackDict


def getPlaylist(id):
    playlistOriginal = sp.playlist(id)
    playlist = playlistOriginal["tracks"]["items"]
    playlistLength = len(playlist)
    
    playlistDict = {}
    playlistDict['type'] = "playlist"
    try:
        playlistDict['name'] = playlistOriginal['name']
    except:
        playlistDict['name']
    try:
        playlistDict['img'] = playlistOriginal['images'][0]['url']
    except:
        playlistDict['img'] = "/static/images/placeholder.png"

    playlistDict['tracks'] = {}
    
    for i in range(playlistLength):
        playlistDict['tracks'][i+1] = {}
        
        track = playlist[i]["track"]
        try:
            artists = track["artists"]
        except:
            artists = ""
            
        trackArtists = []
        for j in range(len(artists)):
            trackArtists.append(artists[j]["name"])
        
        try:
            trackName = track["name"]
        except:
            trackName = ""
        try:
            trackId = track["id"]
        except:
            trackId = ""
            
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
        except:
            trackDuration = None
        
        playlistDict['tracks'][i+1] = {
            "track": trackName, 
            "artists" : trackArtists, 
            "loudness" : trackLoudness,  
            "danceability" : trackDanceability, 
            "valence" : trackValence,
            "instrumentalness" : trackInstrumentalness,
            "speechiness" : trackSpeechiness,
            "acousticness" : trackAcousticness,
            "key" : trackKey + " " + trackMode,
            "duration" : trackDuration
            }
        
    return playlistDict


def getArtistAlbums(id):
    albums = sp.artist_albums(id, limit=50)
    artist = sp.artist(id)
    albumsDict = {}
    albumsDict['type'] = "artist"
    albumsDict['artists'] = [artist['name']]
    try:
        albumsDict['img'] = artist['images'][0]['url']
    except:
        albumsDict['img'] = "/static/images/artistplaceholder.png"
    albumsDict['albums'] = {}
    albumsDict['singles'] = {}
    albumsDict['compilations'] = {}
    
    for i in range(len(albums['items'])):
        if albums['items'][i]['album_type'] == "album":
            albumsDict['albums'][albums['items'][i]['name']] = {}
            albumsDict['albums'][albums['items'][i]['name']]['id'] = albums['items'][i]['id']
            albumsDict['albums'][albums['items'][i]['name']]['release'] = albums['items'][i]['release_date']
            try:
                albumsDict['albums'][albums['items'][i]['name']]['img'] = albums['items'][i]['images'][0]['url']
            except:
                albumsDict['albums'][albums['items'][i]['name']]['img'] = "/static/imgages/placeholder.png"
        if albums['items'][i]['album_type'] == "single":
            albumsDict['singles'][albums['items'][i]['name']] = {}
            albumsDict['singles'][albums['items'][i]['name']]['id'] = albums['items'][i]['id']
            albumsDict['singles'][albums['items'][i]['name']]['release'] = albums['items'][i]['release_date']
            try:
                albumsDict['singles'][albums['items'][i]['name']]['img'] = albums['items'][i]['images'][0]['url']
            except:
                albumsDict['singles'][albums['items'][i]['name']]['img'] = "/static/imgages/placeholder.png"
        if albums['items'][i]['album_type'] == "compilation":
            albumsDict['compilations'][albums['items'][i]['name']] = {}
            albumsDict['compilations'][albums['items'][i]['name']]['id'] = albums['items'][i]['id']
            albumsDict['compilations'][albums['items'][i]['name']]['release'] = albums['items'][i]['release_date']
            try:
                albumsDict['compilations'][albums['items'][i]['name']]['img'] = albums['items'][i]['images'][0]['url']
            except:
                albumsDict['compilations'][albums['items'][i]['name']]['img'] = "/static/imgages/placeholder.png"
            
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
        minutes = int((value/1000)/60)
        seconds = (value/1000) % 60
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
    return value.replace('"','').upper()

def releaseYear(value):
    return value[:4]