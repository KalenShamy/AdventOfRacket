from django.db import models
from mongoengine import Document, StringField, IntField, BooleanField, DateTimeField, ListField, ReferenceField
from datetime import datetime
from zoneinfo import ZoneInfo

# Create your models here.

class User(Document):
    github_id = IntField(required=True, unique=True)
    username = StringField(required=True)
    url = StringField(required=True)
    avatar_url = StringField()
    access_token = StringField()
    created_at = DateTimeField(default=datetime.now())
    problems = ListField(ListField(ReferenceField('Problem')))

    def __str__(self):
        return f"{self.name}"
    
class Problem(Document):
    player = StringField(required=True)
    day = IntField(required=True)
    part = IntField(required=True)  # 1 or 2
    time_started = DateTimeField(default=datetime.now())
    code = StringField()
    correct = BooleanField(default=False)
    time_taken = IntField()  # in seconds
    total_time = IntField()  # in seconds, cumulative time including previous parts
    tests = ListField(StringField())  # list of [user_output] (index aligns with test cases)
    tests_message = StringField()  # message about the tests, e.g. "All tests passed" or "3/5 tests passed"

    def __str__(self):
        return f"Submission by {self.player} for {self.day}.{self.part} taking {self.time_taken} seconds"