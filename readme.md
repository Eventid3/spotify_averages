# Spotify Averages
### Video Demo:  <https://youtu.be/KTWBpE7JwGA>
### Description:
My final project for CS50 is Spotify Averages.
The project is somewhat inspired by the Week 7 Lab: Songs. My background is in music production, and I found the info on that perticular lab quite interesting.
Spotify Averages is a Flask application, that pulls audio analysis data from Spotify, via a Python library called Spotipy. This data is then shown to the user in a few different ways.
Firstly, the official "Top Hits" playlists from each year are available to lookup - all the way back from 1970. Secondly, the data from the "Top Hits" playlists are averaged, so they can be viewed over time - showing some interesting long term trends in the evolution of music over the years. Getting this amount of data fast required use of SQL databases.
Lastly, there's a search feature, where the user can look up any of their favorite tracks, artists or albums on Spotify, and get their audio analysis.

### Getting started:
To run the app locally, a virtual environment needs to be set up, and Spotipy needs a client id and a secret key, to allow access to Spotify's data. A client id and secret key can be accessed by making a dummy test project on the Spotify for Developers website: <https://developer.spotify.com/dashboard/login> 

```
python3 -m venv venv
export SPOTIPY_CLIENT_ID='client id'
export SPOTIPY_CLIENT_SECRET='secret key'
```

Now the application is ready to run with:
```
flask run
```

### Files
#### auth.py
This is a simple file, that ensures the authentication process from Spotipy to Spotify.
The 'sp' variable will be used often throughout the app.

#### sql_converter.py
Calculation averages from 50+ playlists each containing 100 songs takes some time, especially when the requests are pulled from Spotify through Spotify. Therefore, the "Top Hits" playlists are converted to SQL databases (SpotifyTopHits.db) for much quicker local access.
In this code (and thoughout the rest of the app) some more or less complex dictionary slicing is required, since the data pulled from Spotify is quite extensive.
Also, alot of "try" and "except" are used to avoid errors if a song is missing some data, an image file etc.

This file is not used during runtime of the app.

#### constants.py
Just a few constant dictionaries containing the Spotify id's of the "Top Hits" playlists, and also a trackKeyDict used to convert the key of a song from an int to a string.

#### app.py
This is the main app controlling all of the routes in the app.
At the top, the app is initialized and some filters for jinja is set up.

The index function simply controls the root route - nothing fancy here.

The tophits controls the section of the same name, returning the user requested year while also checking for invalid input.

Averages for checks for the user requested data parameter, then retrieves the average of this parameter from all of the years in the sql database, and returns it to the user in the form of a chart, via a javascript library called chart.js. 
Some of the data is presented in a value from 0.0 to 1.0. In my opinion this isn't very user friendly, so I chose to show it in percent instead. 
In the other section in the app, a jinja filter is used to convert the data to percent, but when sending the data to chart.js, I simply multiply by 100 (or divide by 1000, in the case of converting milliseconds to seconds)

The search section is quite simply, in that it just requests a seqrch query from the user, sends it to Spotify via Spotipy, and returns the results - after a try/except block, to prevent any failures in the search.

Lookup is used when the user chooses to lookup any of the returned search results. Lookup recieves both an id and a category from the user, since different Spotipy functions is required for songs, albums, playlists and artists.

Lastly, info just returns the info section.

#### functions.py
Whenever a function is called in app.py, it's a function located in functions.py. Most of the functions here are functiions that first sends a search or id request to Spotify vis Spotipy, and then extracts the relevant data after errorchecking. Again, alot of slicing into dictionaries is going on here.

The jinja filter functions are also located here.

#### static files
In here there's some basic css styling, some images and some js used for the chart.js instance and showing and hiding the navbar when using the app on a mobile device.
While the the website is made in a responsive design, the best experience is on a bigger screen, since large tables with lots of data is better shown there.

#### templates
Html templates here. The most complex of the bunch is the lookup.html, since the app needs to handle a few different types of returned data, depending on whether it's an album, a song or an artist's data thats being shown.