from typing import Any
from django.db import models
from django.utils.safestring import mark_safe


class Banners(models.Model):
    img = models.ImageField(upload_to="banners")
    alt_text = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.alt_text
    
    def image_tag(self):
        return mark_safe('<img src="%s" width ="80"/>' %(self.img.url))

class Service(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField(max_length=150)
    img = models.ImageField(upload_to="services")

    def __str__(self) -> str:
        return self.title
    
    def image_tag(self):
        return mark_safe('<img src="%s" width ="80"/>' %(self.img.url))

class Page(models.Model):
    title = models.TextField(max_length=100)
    detail = models.TextField(max_length=100)

    def __str__(self):
        return self.title
    

class Faq(models.Model):
    question = models.TextField(max_length=100)
    answer = models.TextField(max_length=100)

    def __str__(self):
        return self.question