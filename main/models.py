from django.db import models
from django.utils.safestring import mark_safe


class Banners(models.Model):
    img =models.ImageField(upload_to="banners")
    alt_text = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.alt_text
    
    def image_tag(self):
        return mark_safe('<img src="%s" width ="80"/>' %(self.img.url))