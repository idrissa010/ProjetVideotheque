# app2/controllers/video_controller.py
from flask import Blueprint, request, jsonify
from app2.services.video_service import VideoService
from app2.models.video import Video
import uuid
from flask_jwt_extended import get_jwt_identity, jwt_required

video_bp = Blueprint('video', __name__)

@video_bp.route('/videos', methods=['GET'])
def get_videos():
    VideoService.load_videos()
    videos = VideoService.get_videos()
    return jsonify([vars(video) for video in videos]), 200


@video_bp.route('/videos/<owner_id>', methods=['GET'])
@jwt_required()  
def get_videos_by_owner(owner_id):
    VideoService.load_videos()
    videos = VideoService.get_video_by_owner(owner_id)
    return jsonify([vars(video) for video in videos]), 200


@video_bp.route('/videos/<owner_id>/<video_id>', methods=['GET'])
@jwt_required()  
def get_video_by_id(owner_id, video_id):
    VideoService.load_videos()
    videos = VideoService.get_video_by_owner(owner_id)
    video = next((video for video in videos if video.id == video_id), None)
    print(video)
    if video:
        return jsonify(vars(video)), 200
    else:
        return jsonify({'message': 'Video not found'}), 404
    
    
@video_bp.route('/videos', methods=['POST'])
@jwt_required()  
def add_video():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    video_id = str(uuid.uuid4())  # Générer un ID unique
    data['id'] = video_id  # Ajouter l'ID à vos données de vidéo
    data['owner_id'] = current_user_id  # Ajouter l'ID du User à vos données de vidéo
    video = Video(**data)
    VideoService.add_video(video)
    return jsonify({'message': 'Video added successfully'}), 201


@video_bp.route('/videos/<owner_id>/<id>', methods=['PUT'])
@jwt_required()  
def update_video(owner_id, id):
    VideoService.load_videos()
    videos = VideoService.get_video_by_owner(owner_id)
    video = next((video for video in videos if video.id == id), None)

    if video:
        data = request.get_json()
        for key, value in data.items():
            setattr(video, key, value)
        VideoService.save_videos()
        return jsonify({'message': 'Video updated successfully'}), 200
    else:
        return jsonify({'message': 'Video not found'}), 404


@video_bp.route('/videos/<owner_id>/<id>', methods=['DELETE'])
@jwt_required()  
def delete_video(owner_id, id):
    VideoService.load_videos()
    videos = VideoService.get_video_by_owner(owner_id)
    video = next((video for video in videos if video.id == id), None)

    if video:
        VideoService.videos.remove(video)
        VideoService.save_videos()
        return jsonify({'message': 'Video deleted successfully'}), 200
    else:
        return jsonify({'message': 'Video not found'}), 404


