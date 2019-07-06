from django.db import models


class Event(models.Model):
    """
    Event model
    """
    id = models.BigIntegerField(primary_key=True, unique=True)
    type = models.ForeignKey('Type', on_delete=models.CASCADE, null=True, related_name="events")
    actor = models.ForeignKey('Actor', on_delete=models.CASCADE, null=True, related_name='events')
    repo = models.ForeignKey('Repo', on_delete=models.CASCADE, null=True, related_name="events")


class Actor(models.Model):
    """
    Actor model
    """
    id = models.BigIntegerField(primary_key=True, unique=True)
    login = models.CharField(max_length=30, unique=True, null=True)
    avatar_url = models.URLField(null=True)


class Repo(models.Model):
    """
    Repository model
    """
    id = models.BigIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=200, null=True)
    url = models.URLField(null=True, unique=True)


class Type(models.Model):
    name = models.CharField(max_length=100, unique=True)
