# app2/models/video.py
import uuid

class Video:
    def __init__(self, owner_id, title, genre, age, release_year, country, duration, quality, is_movie, description):
        self.id = str(uuid.uuid4())
        self.owner_id = owner_id
        self.title = title
        self.genre = genre
        self.age = age
        self.release_year = release_year
        self.country = country
        self.duration = duration
        self.quality = quality
        self.is_movie = is_movie
        self.description = description
    # def __init__(self, title, director, main_actors, genre, release_year, country, duration, language, format, is_public, note, comments, owner_id, location, synopsis, summary):
    #     self.title = title
    #     self.director = director
    #     self.main_actors = main_actors
    #     self.genre = genre
    #     self.release_year = release_year
    #     self.country = country
    #     self.duration = duration
    #     self.language = language
    #     self.format = format
    #     self.is_public = is_public
    #     self.note = note
    #     self.comments = comments
    #     self.owner_id = owner_id
    #     self.location = location
    #     self.synopsis = synopsis
    #     self.summary = summary

    def to_dict(self):
        return vars(self)
