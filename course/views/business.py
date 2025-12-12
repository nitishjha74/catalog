from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from course.services.business import SkillVideoService
from course.serializers.business import SkillVideoSerializer

from course.authentication.business import SSOBusinessTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SkillVideoCreateView(APIView):
    authentication_classes = [SSOBusinessTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Upload business skill video (YouTube link)",
        operation_description="""
        Business uploads a YouTube video link which will be locked inside JSJ Skill.
        Only paid users can watch the locked video.

        System extracts YouTube video ID automatically and stores it.
        """,
        tags=["JSJ Skill"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["youtube_url", "title"],
            properties={
                "youtube_url": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="https://www.youtube.com/watch?v=abcd1234",
                    description="Full YouTube video URL"
                ),
                "title": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Learn Retail Marketing",
                    description="Video title"
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="This video teaches retail marketing techniques.",
                    description="Optional description"
                ),
            }
        ),
        responses={
            201: openapi.Response(
                description="Video uploaded successfully",
                schema=SkillVideoSerializer
            ),
            400: "Bad Request",
            500: "Internal Server Error"
        }
    )
    def post(self, request):

        try:
            video = SkillVideoService.create_skill_video(
                request.user.business_id,
                request.data
            )

            serializer = SkillVideoSerializer(video)
            return Response(
                {"message": "Skill video created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )

        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"message": "Unexpected error", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SkillVideoDetailView(APIView):
    authentication_classes = [SSOBusinessTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Fetch skill video + YouTube stats",
        tags=["JSJ Skill"],
        manual_parameters=[
            openapi.Parameter(
                "video_id",
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={200: SkillVideoSerializer()}
    )
    def get(self, request):
        video_id = request.query_params.get("video_id")

        video = SkillVideoService.get_video_by_id(video_id)

        if not video:
            return Response({"message": "Video not found"}, status=404)

        serializer = SkillVideoSerializer(video)

        youtube_stats = SkillVideoService.get_youtube_stats(video.youtube_video_id)

        return Response(
            {
                "video": serializer.data,
                "youtube_stats": youtube_stats
            },
            status=200
        )
