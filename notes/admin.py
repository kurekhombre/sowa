from django.contrib import admin
from .models import Topic, Note, Record
# Register your models here.

admin.site.register(Topic)
admin.site.register(Note)
admin.site.register(Record)
