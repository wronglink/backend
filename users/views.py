from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.models import ME_ALIAS, Followings
from users.permissions import UserRegistrationOrThemselfOrReadOnly
from users.serializers import UserSerializer, FollowingSerializer, FollowedSerializer, FollowsSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [UserRegistrationOrThemselfOrReadOnly]

    def get_object(self):
        if self.kwargs[self.lookup_field] == ME_ALIAS:
            self.kwargs[self.lookup_field] = self.request.user.username
        return super(UsersViewSet, self).get_object()

    @action(detail=True)
    def followed(self, request, username):
        username = request.user.username if username == ME_ALIAS else username
        queryset = Followings.objects.filter(follows__username=username)
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(FollowedSerializer(page, many=True).data)
        return Response(FollowedSerializer(page, many=True).data)

    @action(detail=True)
    def follows(self, request, username):
        username = request.user.username if username == ME_ALIAS else username
        queryset = Followings.objects.filter(follower__username=username)
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(FollowsSerializer(page, many=True).data)
        return Response(FollowsSerializer(page, many=True).data)


class FollowingsViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Followings.objects
    serializer_class = FollowingSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'follows__username'
    lookup_url_kwarg = 'username'

    def create(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
        except Http404:
            serializer = self.get_serializer(data={'follows': self.kwargs[self.lookup_url_kwarg]})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save(follower=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(follower=self.request.user)
