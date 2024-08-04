from django.db import models

from config import settings
from materials.validators import validate_video_link


# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to="course_previews/", blank=True, null=True)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video_link = models.URLField(validators=[validate_video_link])

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    preview = models.ImageField(upload_to="lesson_previews/", blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    course = models.ForeignKey(
        Course, related_name="subscriptions", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="subscriptions", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ["course", "user"]
