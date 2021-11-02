from flask_pymongo import pymongo
from pymongo import MongoClient


CONNECTION_STRING = "mongodb+srv://malia-barker:NowbpedOY0I9bVme@playlistr-mb.jmhsu.mongodb.net/playlistr?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_default_database()

playlists = db.playlists
comments = db.comments

from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId

app = Flask(__name__)
def video_url_creator(id_lst):
    videos = []
    for vid_id in id_lst:
        # We know that embedded YouTube videos always have this format
        video = 'https://youtube.com/embed/' + vid_id
        videos.append(str(video))

    return videos

@app.route('/')
def playlists_index():
    """Show playlists"""
    return render_template('playlists_index.html', playlists=playlists.find())

@app.route('/playlists/new')
def playlists_new():
    """Create new playlist"""
    return render_template('playlists_new.html', playlist={}, title='New Playlist')

# Note the methods parameter that explicitly tells the route that this is a POST
@app.route('/playlists', methods=['POST'])
def playlists_submit():
    """Submit a new playlist."""
    # Grab the video IDs and make a list out of them
    video_ids = str(request.form.get('video_ids')).split()
    # call our helper function to create the list of links
    videos = video_url_creator(video_ids)
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': videos,
        'video_ids': video_ids
    }
    playlists.insert_one(playlist)
    return redirect(url_for('playlists_index'))

@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    """Show single playlist"""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    playlist_comments = comments.find({'playlist_id': playlist_id})
    return render_template('playlists_show.html', playlist=playlist, comments=playlist_comments)

@app.route('/playlists/<playlist_id>/edit')
def playlists_edit(playlist_id):
    """Edit single playlist"""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_edit.html', playlist=playlist, title='Edit Playlist')

@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlists_update(playlist_id):
    '''Submit edited playlist'''
    video_ids = str(request.form.get('video_ids')).split()
    videos = video_url_creator(video_ids)
    #create updated playlist 
    updated_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': videos,
        'video_ids': video_ids
    }
    #set formed playlist to new update
    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_playlist}
    )
    #take us back to playlist show page
    return redirect(url_for('playlists_show', playlist_id=playlist_id))

@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def playlists_delete(playlist_id):
    """Delete a playlist"""
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))

@app.route('/playlists/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'playlist_id': request.form.get('playlist_id'),
        'title' : request.form.get('title'),
        'content' : request.form.get('content')
    }
    comments.insert_one(comment)
    return redirect(url_for('playlists_show', playlist_id=request.form.get('playlist_id')))


if __name__ == '__main__':
    app.run(debug=True, port=8000)