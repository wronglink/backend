from django.db import models

# Create your models here.
ME_ALIAS = 'me'


class Followings(models.Model):
    follower = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='follows')
    follows = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='followed')
    followed = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-followed']
        unique_together = ('follower', 'follows')
