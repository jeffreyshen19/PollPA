from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from datetime import datetime

class Poll(models.Model):
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    available = models.DateTimeField(db_index=True)
    closes = models.DateTimeField(db_index=True)
    text = models.TextField()
    description = models.TextField()

class AuthToken(models.Model):
    username = models.TextField()
    identifier = models.TextField(unique=True)
    expires = models.DateTimeField()
    metadata = models.TextField(default="{}")
    single_use = models.BooleanField(default=True)

    def get_user_and_activate(self):
        if self.expires > datetime.utcnow():
            return None
        user = User.objects.get(username=self.username)
        if user == None:
            password = get_random_string()
            user = User.objects.create_user(self.username, email=self.username, password=password)
            # TODO: send signup email
        if self.single_use:
            self.delete()
        return user

""" Supplement model for custom user data. Think of it as a user's settings. """
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.IntegerField()
    send_emails = models.BooleanField(default=True)

""" Indicates _whether_ a user has voted. Does not contain the vote
 itself. This allows votes to be truthfully and absolutely separated
 from individual users, rendering votes completely anonymous—even
 to someone with full access to the database.
""" 
class VoteFingerprint(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.TextField()
    description = models.TextField()

class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    description = models.TextField()

class Vote(models.Model):
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    year = models.IntegerField()

class VoteChoice(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(QuestionOption, on_delete=models.CASCADE)