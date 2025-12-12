from django.db import models

# Create your models here.
class SkillVideo(models.Model):
    business = models.IntegerField(verbose_name="Business ID")

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    youtube_url = models.CharField(
        max_length=50,
        help_text="Extracted YouTube Video ID (e.g., dQw4w9WgXcQ)"
    )

    is_locked = models.BooleanField(
        default=True,
        help_text="If True → only paid users can watch"
    )
    youtube_video_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.youtube_video_id})"


class SkillInterest(models.Model):
    video = models.ForeignKey(SkillVideo, on_delete=models.CASCADE)
    mbrcardno = models.IntegerField()
    interested_at = models.DateTimeField(auto_now_add=True)

   