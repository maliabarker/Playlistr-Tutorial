from flask import Flask, render_template

app = Flask(__name__)

# @app.route('/')
# def index():
#     """Return homepage"""
#     return render_template('home.html', msg="Flask is Cool!")

playlists = [
    { 'title': 'Cat Videos', 'description': 'Cats acting weird'},
    { 'title': 'Doja Cat', 'description': 'The best artist in the world'}
]

@app.route('/')
def playlists_index():
    """Show playlists"""
    return render_template('playlists_index.html', playlists=playlists)

if __name__ == '__main__':
    app.run(debug=True)