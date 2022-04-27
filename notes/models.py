from django.db import models
from django.urls import reverse
from users.models import Profile
import uuid
# Create your models here.


class Topic(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def get_absolute_url(self):
        return reverse('topic-list')

    def __str__(self):
        return str(self.title)


class Note(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=128)
    summary = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.title)


class Record(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, null=True, blank=True)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f'{self.key} | {self.value}'