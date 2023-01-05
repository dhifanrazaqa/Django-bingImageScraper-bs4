from django.db import models
from datetime import datetime
from django.template.defaultfilters import slugify

class Post(models.Model):
    keyword = models.CharField(max_length=200)
    url = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length = 1000, null=True, blank=True, unique=True)
    date_modified = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.keyword

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.keyword + "-" + str(datetime.date(datetime.now())) + str(datetime.now())[-6:])
        return super().save(*args, **kwargs)

class imagePost(models.Model):
    imageTitle = models.CharField(max_length=200)
    imageURL = models.TextField(null=True, blank=True)
    imageURLHD = models.TextField(null=True, blank=True)
    imageDescription = models.TextField(null=True, blank=True)
    imageKeyword = models.ForeignKey(Post, on_delete=models.CASCADE)
    slugImage = models.CharField(max_length = 1000, null=True, blank=True)
    slugImageDetail = models.CharField(max_length = 1000, null=True, blank=True, unique=True)

    def __str__(self):
        return self.imageTitle

    def save(self, *args, **kwargs):
        if not self.slugImage:
            self.slugImage = self.imageKeyword.slug
        if not self.slugImageDetail:
            self.slugImageDetail = slugify(self.imageTitle + "-" + str(datetime.date(datetime.now())) + str(datetime.now())[-6:])
        return super().save(*args, **kwargs)
