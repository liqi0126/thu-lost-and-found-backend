from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30)
    # Hex color codes, eg: #FFFFFF, default to light blue color
    color = models.CharField(max_length=7, blank=True, default='#116bee')
    extra = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
