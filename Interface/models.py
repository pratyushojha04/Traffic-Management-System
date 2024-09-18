from django.db import models
import uuid

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    session_id = models.UUIDField(default=uuid.uuid4, editable=False)  # Track the session
