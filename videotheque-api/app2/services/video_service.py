# app2/services/video_service.py
import json
from app2.models.video import Video
from config import JSON_VIDEO_DATABASE_PATH

class VideoService:
    videos = []

    @classmethod
    def load_videos(cls):
        try:
            with open(JSON_VIDEO_DATABASE_PATH, 'r') as file:
                content = file.read()
                if not content:
                    print("Le fichier JSON est vide.")
                    cls.videos = []
                    return
                videos_data = json.loads(content)
        except FileNotFoundError:
            print(f"Fichier JSON introuvable à l'emplacement {JSON_VIDEO_DATABASE_PATH}.")
            videos_data = []
        except json.JSONDecodeError as e:
            print(f"Erreur de décodage JSON : {e}")
            videos_data = []

        # Exclure la clé 'created_at' du dictionnaire video_data
        filtered_videos_data = [{k: v for k, v in video_data.items() if k != 'created_at'} for video_data in videos_data]

        # Instancier la classe Video avec les données filtrées
        cls.videos = [Video(**video_data) for video_data in filtered_videos_data]
    # def load_videos(cls):
    #     try:
    #         with open(JSON_VIDEO_DATABASE_PATH, 'r') as file:
    #             content = file.read()
    #             if not content:
    #                 # Le fichier est vide, gérer en conséquence
    #                 print("Le fichier JSON est vide.")
    #                 cls.videos = []
    #                 return
    #             videos_data = json.loads(content)
    #     except FileNotFoundError:
    #         print(f"Fichier JSON introuvable à l'emplacement {JSON_VIDEO_DATABASE_PATH}.")
    #         videos_data = []
    #     except json.JSONDecodeError as e:
    #         print(f"Erreur de décodage JSON : {e}")
    #         videos_data = []

    #     cls.videos = [Video(**video_data) for video_data in videos_data]

    @classmethod
    def save_videos(cls):
        videos_data = [video.to_dict() for video in cls.videos]
        
        print(f"Nombre de vidéos à sauvegarder : {len(cls.videos)}")
        print(f"Contenu des vidéos à sauvegarder : {videos_data}")

        with open(JSON_VIDEO_DATABASE_PATH, 'w') as file:
            json.dump(videos_data, file)
            print("Videos saved successfully")

    @classmethod
    def add_video(cls, video):
        cls.load_videos()  # Charge les vidéos actuelles
        print(f"Nombre de vidéos avant l'ajout : {len(cls.videos)}")
        cls.videos.append(video)
        cls.save_videos()
        print(f"Nombre de vidéos après l'ajout : {len(cls.videos)}")



    @classmethod
    def get_videos(cls):
        cls.load_videos()
        return cls.videos

    @classmethod
    def get_video_by_owner(cls, owner_id):
        return [video for video in cls.videos if video.owner_id == owner_id]
