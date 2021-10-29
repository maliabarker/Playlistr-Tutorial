from pymongo import MongoClient

client = MongoClient()
db = client.Playlistr
playlists = db.playlists

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def video_url_creator(id_lst):
    videos = []
    for vid_id in id_lst:
        video = 'https://youtube.com/embed/' + vid_id
        videos.append(video)
        print(videos)
    return videos

@app.route('/')
def playlists_index():
    """Show playlists"""
    return render_template('playlists_index.html', playlists=playlists.find())

@app.route('/playlists/new')
def playlists_new():
    """Create new playlist"""
    return render_template('playlists_new.html')

@app.route('/playlists', methods=['POST'])
def playlists_submit():
    """Submit new playlist"""
    video_ids = str(request.form.get('video_ids')).split()
    videos = video_url_creator(video_ids)
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': videos,
        'video_ids': video_ids
    }
    playlists.insert_one(playlist)
    print(request.form.to_dict())
    return redirect(url_for('playlists_index'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)