import re

from django.core.exceptions import ValidationError


def validate_video_link(value):
    youtube_regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$"  # Copy-pasted from internet
    if not re.match(youtube_regex, value):
        raise ValidationError("Invalid YouTube video link.")
