from pymongo import MongoClient

client = MongoClient()
db = client.Playlistr
playlists = db.playlists

from flask import Flask, render_template

app = Flask(__name__)

# playlists = [
#     { 'title': 'Cat Videos', 'description': 'Cats acting weird'},
#     { 'title': 'Doja Cat', 'description': 'The best artist in the world'}
# ]

@app.route('/')
def playlists_index():
    """Show playlists"""
    return render_template('playlists_index.html', playlists=playlists.find())

if __name__ == '__main__':
    app.run(debug=True, port=8000)