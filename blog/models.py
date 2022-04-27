from django.db import models
import uuid


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    author = models.CharField(max_length=64)
    image = models.ImageField(default='default.jpg', upload_to='blog_articles',null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['-created']