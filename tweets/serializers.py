from rest_framework import serializers

from tweets.models import Tweet
from users.serializers import UserSerializer


class TweetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'text', 'photo', 'author', 'created']
