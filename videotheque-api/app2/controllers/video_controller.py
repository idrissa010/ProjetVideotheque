# app2/controllers/video_controller.py
from flask import Blueprint, request, jsonify
from app2.services.video_service import VideoService
from app2.models.video import Video

video_bp = Blueprint('video', __name__)

@video_bp.route('/videos', methods=['GET'])
def get_videos():
    VideoService.load_videos()
    videos = VideoService.get_videos()
    return jsonify([vars(video) for video in videos]), 200

@video_bp.route('/videos/<owner_id>', methods=['GET'])
def get_videos_by_owner(owner_id):
    VideoService.load_videos()
    videos = VideoService.get_video_by_owner(owner_id)
    return jsonify([vars(video) for video in videos]), 200

@video_bp.route('/videos', methods=['POST'])
def add_video():
    data = request.get_json()
    video = Video(**data)
    VideoService.add_video(video)
    return jsonify({'message': 'Video added successfully'}), 201

@video_bp.route('/videos/<owner_id>/<title>', methods=['PUT'])
def update_video(owner_id, title):
    VideoService.load_videos()
    videos = VideoService.get_video_by_owner(owner_id)
    video = next((video for video in videos if video.title == title), None)

    if video:
        data = request.get_json()
        for key, value in data.items():
            setattr(video, key, value)
        VideoService.save_videos()
        return jsonify({'message': 'Video updated successfully'}), 200
    else:
        return jsonify({'message': 'Video not found'}), 404

@video_bp.route('/videos/<owner_id>/<title>', methods=['DELETE'])
def delete_video(owner_id, title):
    VideoService.load_videos()
    videos = VideoService.get_video_by_owner(owner_id)
    video = next((video for video in videos if video.title == title), None)

    if video:
        VideoService.videos.remove(video)
        VideoService.save_videos()
        return jsonify({'message': 'Video deleted successfully'}), 200
    else:
        return jsonify({'message': 'Video not found'}), 404
