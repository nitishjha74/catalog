from django.urls import path
from course.views import business, member

urlpatterns = [
    path("business/skill-video/create/", business.SkillVideoCreateView.as_view(), name="skill-video-create"),
    path("business/skill-video/detail/", business.SkillVideoDetailView.as_view(), name="skill-video-detail"),


    path("member/skill-video/list/", member.VideoList.as_view(), name="skill-video-list"),

]
