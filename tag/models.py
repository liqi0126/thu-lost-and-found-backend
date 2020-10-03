from django.db import models
from property.models import Property


class Tag(models.Model):
    content = models.TextField(unique=True)
    properties = models.ManyToManyField(Property, related_name='tags')
