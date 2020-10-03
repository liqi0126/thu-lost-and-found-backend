from django.db import models
from django.core import validators

class Property(models.Model):
    name = models.CharField(max_length=30)
    descriptions = models.TextField()

    # TODO: how to enumerate different kind of properties ?
    # TODO: how to determine this is a lost property or found property ?

    # OnetoOneField
    # found_notice
    # lost_notice

    # ForeignKey
    # tags


class SchoolCard(models.Model):
    school_id = models.CharField(validators=[validators.RegexValidator("[12]\d{9}",message='Please Enter the right school id!')],
                             max_length=10, primary_key=True)
    property = models.OneToOneField(Property, on_delete=models.CASCADE)


class Phone(models.Model):
    class Model(models.TextChoices):
        IPHONE5 = 'IP5'
        IPHONE6 = 'IP6'
        IPHONEX = 'IPX'
        IPHONE11 = 'IP11'

    model = models.CharField(max_length=4, choices=Model.choices, default=Model.IPHONEX)
    property = models.OneToOneField(Property, on_delete=models.CASCADE)


class Book(models.Model):
    name = models.TextField(max_length=30)
    author = models.TextField(max_length=30)
    property = models.OneToOneField(Property, on_delete=models.CASCADE)