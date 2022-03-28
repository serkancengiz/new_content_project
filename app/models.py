from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Channel(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(null=False, blank=True, unique=True, db_index=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Content(models.Model):
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to="contents")
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(null=False, blank=True, unique=True, db_index=True, editable=False)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ContentDetails(models.Model):
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to="content_details")
    file = models.FileField(upload_to="content_details")
    description_detail = models.TextField()
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(null=False, blank=True,  unique=True, db_index=True, editable=False)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    cont = models.ForeignKey(Content, on_delete=models.CASCADE)
    votes = models.IntegerField()

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)



