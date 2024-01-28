# app2/models/video.py
from datetime import datetime

class Video:
    def __init__(self, id, owner_id, title, genre, age, release_year, country, duration, quality, category, description, rating):
        self.id = id
        self.owner_id = owner_id
        self.title = title
        self.genre = genre
        self.age = age
        self.release_year = release_year
        self.country = country
        self.duration = duration
        self.quality = quality
        self.category = category
        self.description = description
        self.rating = rating
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'owner_id' : self.owner_id,
            'title' : self.title,
            'genre' : self.genre,
            'age' : self.age,
            'release_year' : self.release_year,
            'country' : self.country,
            'duration' : self.duration,
            'quality' : self.quality,
            'category' : self.category,
            'description' : self.description,
            'rating' : self.rating,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
