from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from chat.models import *
from chat.utils import random_username_generator, random_id_generator


class FriendListSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id',)


class FriendRequestSerializer(serializers.ModelSerializer):
    friends = FriendListSerializer(many=True, read_only=True)
    player_id = serializers.CharField(max_length=50, write_only=True)
    friend_id = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'friend_id', 'friends')

        extra_kwargs = {
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        friend_id = validated_data.get('id')
        player_id = validated_data.get('id')
        requested_friend = User.objects.get(id=friend_id)
        player = User.objects.get(id=player_id)
        player.friends.add(requested_friend)
        player.save()

        return player
