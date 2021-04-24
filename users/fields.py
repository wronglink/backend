from django.contrib.auth.models import User
from rest_framework.relations import SlugRelatedField


class OtherUserRelatedField(SlugRelatedField):
    def get_queryset(self):
        return User.objects.exclude(username=self.context.get('request').user.username)
