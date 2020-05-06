from bottle import Bottle, run, template, debug, static_file, request
import os, sys
import requests

dirname = os.path.dirname(sys.argv[0])

API_KEY="11c0b99c"
app = Bottle()

def get_movie(movie_id):
    url="http://www.omdbapi.com/?i="+str(movie_id)+"&apikey="+API_KEY
    response = requests.get(url)
    return response.json()


def get_movies(movie_name):
    url="http://www.omdbapi.com/?s="+str(movie_name)+"&apikey="+API_KEY
    response = requests.get(url)
    response = response.json()
    if response:
        movies = response['Search']
        movie_data = {}
        for id, movie in enumerate(movies):
            movie_id = movie['imdbID']
            movie_data[id] = get_movie(movie_id)
            movie_data[id]['Genre'] = movie_data[id]['Genre'].split(',')
            if movie_data[id]['imdbRating'] != 'N/A':
                movie_data[id]['imdbRating'] = str(float(movie_data[id]['imdbRating']) * 10) + '%'
            else:
                movie_data[id]['imdbRating'] = '0%'
            
        return movie_data


@app.route('/', method='GET')
@app.route('/', method='POST')
def index():
    search_results = {}
    if request.method == "POST":
        movie_name = request.forms.get('movie_name')
        search_results = get_movies(movie_name)
  #      print(search_results)
    return template('index.html', movies = search_results)

@app.route('/static/<filename:path>')
def send_static(filename):
    static_f = static_file(filename, root='static/')
    return static_f

run(app, host='0.0.0.0', port=8000)
