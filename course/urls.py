from django.urls import path
from course.views import business

urlpatterns = [
    path("business/skill-video/create/", business.SkillVideoCreateView.as_view(), name="skill-video-create"),
    path("business/skill-video/detail/", business.SkillVideoDetailView.as_view(), name="skill-video-detail"),

]
