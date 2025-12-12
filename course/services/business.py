from course.models import SkillVideo
import requests
from django.conf import settings

class SkillVideoService:

    @staticmethod
    def extract_youtube_video_id(url: str):
        """
        Extract video ID from multiple possible YouTube formats.
        """
        if "v=" in url:
            return url.split("v=")[-1].split("&")[0]

        if "youtu.be/" in url:
            return url.split("youtu.be/")[-1].split("?")[0]

        return None

    @staticmethod
    def create_skill_video(business_id, data):
        """
        Business uploads a new skill video.
        """
        youtube_url = data.get("youtube_url")
        video_id = SkillVideoService.extract_youtube_video_id(youtube_url)

        if not video_id:
            raise ValueError("Invalid YouTube URL format")

        video = SkillVideo.objects.create(
            business=business_id,
            title=data.get("title"),
            description=data.get("description"),
            youtube_url=youtube_url,
            youtube_video_id=video_id,
            is_locked=True,
        )

        return video

    @staticmethod
    def list_business_videos(business_id):
        """
        Fetch all skill videos of a business.
        """
        return SkillVideo.objects.filter(business=business_id).order_by("-created_at")

    @staticmethod
    def get_video_by_id(video_id):
        return SkillVideo.objects.filter(id=video_id).first()


    @staticmethod
    def get_youtube_stats(video_id):
        """
        Fetch views, likes, comments using YouTube Data API v3.
        """

        api_key = settings.YOUTUBE_API_KEY
        url = (
            f"https://www.googleapis.com/youtube/v3/videos"
            f"?part=statistics&id={video_id}&key={api_key}"
        )

        response = requests.get(url).json()

        try:
            stats = response["items"][0]["statistics"]

            return {
                "views": stats.get("viewCount", 0),
                "likes": stats.get("likeCount", 0),
                "comments": stats.get("commentCount", 0)
            }

        except Exception:
            return {"views": 0, "likes": 0, "comments": 0}