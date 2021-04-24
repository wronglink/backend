from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from tweets.models import Tweet
from tweets.permissions import IsAuthorOrReadOnly
from tweets.serializers import TweetSerializer
from users.mixins import ViewSetWithUsernameMixin


class TweetsViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects
    serializer_class = TweetSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        if not self.request.user.is_anonymous:
            return self.queryset.filter(author=self.request.user).all()
        return self.queryset.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserTweetsViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
    ViewSetWithUsernameMixin,
):
    queryset = Tweet.objects
    serializer_class = TweetSerializer

    def get_queryset(self):
        return self.queryset.filter(author__username=self.get_username('parent_lookup_username'))


class FeedViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Tweet.objects
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(author__followed__follower=self.request.user)
