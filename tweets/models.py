from django.db import models


class Tweet(models.Model):
    text = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    photo = models.URLField(max_length=200, blank=True)

    class Meta:
        ordering = ['-created']
