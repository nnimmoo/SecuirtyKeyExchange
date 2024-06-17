from rest_framework import serializers
from .models import Channel
from django.contrib.auth.models import User

class ChannelSerializer(serializers.ModelSerializer):
    sender_user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    recipient_user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Channel
        fields = ['id', 'name', 'sender_user', 'recipient_user', 'accepted', 'initial_sender_secret', 'initial_recipient_secret']
