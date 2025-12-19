from course import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from course.services.member import Meberservice
from course.serializers.business import SkillVideoSerializer

from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class VideoList(APIView):

    def get(self, request):
        videos = Meberservice.videolist()
        serializer = SkillVideoSerializer(videos, many=True)
        return Response(serializer.data)
    
class VideoLike(APIView):
    def post(self, request, video_id):
        access_token = "fmhmsgd"

        videos = Meberservice.like_video(video_id,access_token )
        serializer = SkillVideoSerializer(videos, many=True)
        return Response (serializer.data)