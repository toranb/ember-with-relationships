from django.db import models

class Tag(models.Model):
    description = models.CharField(max_length=100)

class Session(models.Model):
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag)

class Speaker(models.Model):
    name = models.CharField(max_length=100)
    session = models.ForeignKey(Session, blank=True, null=True, related_name='speakers')
