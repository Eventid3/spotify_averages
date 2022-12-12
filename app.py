from flask import (
    Flask,
    render_template,
    request,
    redirect,
    stream_template,
    flash,
    url_for,
)
from functions import (
    getTrack,
    getAlbum,
    getArtistAlbums,
    getPlaylist,
    searchSpotify,
    percent,
    time,
    artists,
    capitalize,
    releaseYear
)
from os import path
from constants import topHitsPlaylists
import sqlite3
import json

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Filters
app.jinja_env.filters["percent"] = percent
app.jinja_env.filters["time"] = time
app.jinja_env.filters["artists"] = artists
app.jinja_env.filters["capitalize"] = capitalize
app.jinja_env.filters["id"] = id
app.jinja_env.filters["releaseYear"] = releaseYear


# Database for top hits
def dict_factory(cursor, row):
    col_names = [col[0] for col in cursor.description]
    return {key: value for key, value in zip(col_names, row)}

# connect to the sql database. check_same_thread needs to be "False" for chart.js to access the data
ROOT = path.dirname(path.realpath(__file__))

db = sqlite3.connect(path.join(ROOT,"SpotifyTopHits.db"), check_same_thread=False)
c = db.cursor()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tophits", methods=["GET", "POST"])
def tophits():
    years = list(topHitsPlaylists.keys())

    if request.method == "POST":
        yearSelected = request.form.get("year")

        if yearSelected is None:
            return stream_template("tophits.html", years=years)

        db.row_factory = dict_factory
        playlist = db.execute("SELECT * FROM TopHits{}".format(yearSelected))

        return stream_template(
            "tophits.html", yearSelected=yearSelected, years=years, playlist=playlist
        )
    else:
        return stream_template("tophits.html", years=years)


@app.route("/averages", methods=["GET", "POST"])
def averages():
    if request.method == "POST":

        parameter = (request.form.get("parameter"),)

        if parameter[0] is None:
            return stream_template("averages.html")

        avgList = []

        for year in topHitsPlaylists:
            avg = c.execute(
                "SELECT AVG(%s) FROM TopHits{}".format(str(year)) % parameter
            )
            if parameter[0] in ["danceability","valence","acousticness","speechiness"]:
                avgList.append(avg.fetchone()[0] * 100)
            elif parameter[0] in ["duration"]:
                avgList.append(avg.fetchone()[0] / 1000)
            else:
                avgList.append(avg.fetchone()[0])

        avgList.reverse()

        return stream_template(
            "averages.html",
            avgList=json.dumps(avgList),
            parameter=json.dumps(parameter[0].capitalize()),
            parameterH2=parameter[0].upper(),
        )
    else:
        return stream_template("averages.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query")
        try:
            results = searchSpotify(query)
        except:
            if query == None or query == "":
                error = "Please enter a valid search query"
            else:
                error = "An error occured!"
            return stream_template("search.html", error=error)

        return stream_template("search.html", results=results)
    else:
        return stream_template("search.html")


@app.route("/lookup", methods=["GET", "POST"])
def lookup():
    if request.method == "POST":
        id = request.form.get("id")
        category = request.form.get("category")

        if category == "albums":
            data = getAlbum(id)
        elif category == "playlists":
            data = getPlaylist(id)
        elif category == "tracks":
            data = getTrack(id)
        elif category == "artists":
            data = getArtistAlbums(id)

        return stream_template("lookup.html", data=data, category=category)
    else:
        return redirect("/search")


@app.route("/info")
def info():
    return stream_template("info.html")
