from course.models import SkillVideo
import requests
from django.conf import settings

class Meberservice:
    @staticmethod
    def videolist():
        return SkillVideo.objects.all()

    @staticmethod
    def like_video(access_token, youtube_video_id):
        url = "https://www.googleapis.com/youtube/v3/videos/rate"

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        params = {
            "id": youtube_video_id,
            "rating": "like"
        }

        response = requests.post(url, headers=headers, params=params)

        if response.status_code == 204:
            return True
        else:
            return response.json()


    def comment_on_video(access_token, youtube_video_id, comment_text):
        url = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "snippet": {
                "videoId": youtube_video_id,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": comment_text
                    }
                }
            }
        }

        response = requests.post(url, headers=headers, json=payload)

        return response.json()
        