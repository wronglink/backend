from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.validators import UniqueTogetherValidator

from users.fields import OtherUserRelatedField
from users.models import Followings, ME_ALIAS


class UserSerializer(serializers.ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'email']

    @classmethod
    def validate_username(cls, value):
        if value == ME_ALIAS:
            raise ValidationError('Username "me" not allowed')
        return value

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data.get('email'),
            first_name=validated_data.get('email'),
            last_name=validated_data.get('email'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class FollowsSerializer(serializers.ModelSerializer):
    follows = UserSerializer(read_only=True)

    class Meta:
        model = Followings
        fields = ['follows', 'followed']


class FollowedSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)

    class Meta:
        model = Followings
        fields = ['follower', 'followed']


class FollowingSerializer(serializers.ModelSerializer):
    follows = OtherUserRelatedField('username')

    class Meta:
        model = Followings
        fields = ['follows', 'followed']
