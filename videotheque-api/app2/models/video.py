# app2/models/video.py
class Video:
    def __init__(self, title, director, main_actors, genre, release_year, country, duration, language, format, is_public, note, comments, owner_id, location, synopsis, summary):
        self.title = title
        self.director = director
        self.main_actors = main_actors
        self.genre = genre
        self.release_year = release_year
        self.country = country
        self.duration = duration
        self.language = language
        self.format = format
        self.is_public = is_public
        self.note = note
        self.comments = comments
        self.owner_id = owner_id
        self.location = location
        self.synopsis = synopsis
        self.summary = summary

    def to_dict(self):
        return vars(self)
