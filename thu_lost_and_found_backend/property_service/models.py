from django.db import models


class PropertyType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    thumbnail = models.ImageField(upload_to='property_type_thumbnails/', null=True, blank=True)
    extra = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)


class PropertyTemplate(models.Model):
    name = models.CharField(max_length=30, unique=True)
    type = models.ForeignKey(PropertyType, on_delete=models.CASCADE, related_name='templates')
    thumbnail = models.ImageField(upload_to='property_template_thumbnails/', null=True, blank=True)
    fields = models.JSONField(default=None)
    extra = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)


class Property(models.Model):
    name = models.CharField(max_length=30)
    template = models.ForeignKey(PropertyTemplate, on_delete=models.CASCADE, related_name='properties')
    attributes = models.JSONField(default=None)
    description = models.CharField(max_length=500, null=True, blank=True)
    extra = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
