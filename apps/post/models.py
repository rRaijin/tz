from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_date = models.DateField(auto_now_add=True, auto_now=False)
    updated_date = models.DateField(auto_now_add=False, auto_now=True)
    is_published = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_short_text(self):
        return '%s...' % self.text[:100]

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'id': self.id})

    class Meta:
        verbose_name_plural = 'Posts'
