from django.contrib import admin
from .models import PropertyType, PropertyTemplate, Property

# Register your models here.
admin.site.register(PropertyType)
admin.site.register(PropertyTemplate)
admin.site.register(Property)