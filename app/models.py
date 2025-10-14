from django.db import models
from mongoengine import Document, StringField, IntField, BooleanField, DateTimeField, ListField, ReferenceField
from datetime import datetime
from zoneinfo import ZoneInfo

eastern_tz_info = ZoneInfo("America/New_York")

# Create your models here.

class User(Document):
    github_id = IntField(required=True, unique=True)
    username = StringField(required=True)
    url = StringField(required=True)
    avatar_url = StringField()
    access_token = StringField()
    created_at = DateTimeField(default=datetime.now(eastern_tz_info))
    problems = ListField(ListField(ReferenceField('Problem')))

    def __str__(self):
        return f"{self.name}"
    
class Problem(Document):
    player = StringField(required=True)
    day = IntField(required=True)
    part = IntField(required=True)  # 1 or 2
    timestamp = DateTimeField(default=datetime.now(eastern_tz_info))
    code = StringField(required=True)
    time_taken = IntField(required=True)  # in seconds

    def __str__(self):
        return f"Submission by {self.player} for {self.day}.{self.part} taking {self.time_taken} seconds"