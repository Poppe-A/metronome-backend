from flask import Blueprint, jsonify, request
from datetime import datetime
import json

from sqlalchemy import func, update
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.songs.models import Song, SongSchema
from app.db_init import db

songs_routes = Blueprint('song_routes', __name__, template_folder='templates')

# SPORTS

@songs_routes.route('/all', methods=['GET'])
def get_songs():
    songs = Song.query.all()
    print("all songs ${songs}")
    return jsonify(SongSchema().dump(songs, many=True))

@songs_routes.route('/add', methods=['POST'])
def add_song():
    print("zoukez")
    data = json.loads(request.data)
    position = getSongPosition()
    song = Song(
        name = data["name"],
        tempo = data["tempo"],
        position = position
    )
    print(song)
    try:
        db.session.add(song)
        res = db.session.commit()
        return get_songs()
        return f"{song.name} added {res}"

    except (SQLAlchemyError, DBAPIError) as e:
        error = str(e.__dict__['orig'])
        return error

@songs_routes.route('/update', methods=['PATCH'])
def update_song():
    data = json.loads(request.data)

    try:
        Song.query.filter(Song.id == data["id"]).update(
            {
                'name': data["name"], 
                'tempo': data["tempo"]
            }
        )
        res = db.session.commit()
        return f"song updated"

    except (SQLAlchemyError, DBAPIError) as e:
        error = str(e.__dict__['orig'])
        return error

@songs_routes.route('/delete/<int:id>', methods=['DELETE'])
def delete_song(id):
    print("id", id)
    # data = json.loads(request.data)

    try:
        print("delete")
        songToDelete = Song.query.get(id)
        db.session.delete(songToDelete)
        db.session.commit()        
        return f"song deleted"

    except (SQLAlchemyError, DBAPIError) as e:
        error = str(e.__dict__['orig'])
        return error

@songs_routes.route('/updateListOrder', methods=['PATCH'])
def update_list_order():
    data = json.loads(request.data)

    # data[oldIndex]
    # data[newIndex]

    orderedSongList = reOrderSongs(data['oldIndex'], data['newIndex'])
    return f"cool"
    # try:
    #     Song.query.filter(Song.id == data["id"]).update(
    #         {
    #             'name': data["name"], 
    #             'tempo': data["tempo"]
    #         }
    #     )
    #     res = db.session.commit()
    #     return f"song updated"

    # except (SQLAlchemyError, DBAPIError) as e:
    #     error = str(e.__dict__['orig'])
    #     return error
  

def getSongPosition():
    position = db.session.query(func.max(Song.position)).first()

    if (None in position):
        return 0
    else:
        return position[0] + 1

def reOrderSongs(oldIndex, newIndex):
    songs = Song.query.order_by(Song.position).all()
    songToChange = next((song for song in songs if song.position == oldIndex), None)

    # We apply to different calculation depending on the values of indexes.
    # Please refer to the repo's readme to understand the algo

    for song in songs:
        if ((oldIndex < newIndex) and (song.position > oldIndex) and (song.position < newIndex)):
            song.position = song.position - 1
        elif ((oldIndex > newIndex) and (song.position >= newIndex) and (song.position < oldIndex)):
            song.position = song.position + 1
        if (song.id == songToChange.id ):
            song.position = newIndex - 1 if oldIndex < newIndex else newIndex

        try:
            Song.query.filter(Song.id == song.id).update(
                {
                    'position': song.position
                }
            )
            db.session.commit()

        except (SQLAlchemyError, DBAPIError) as e:
            error = str(e.__dict__['orig'])
            return error

    return songs