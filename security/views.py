from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import ChannelSerializer
import os
import random
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import Channel
from rest_framework.response import Response
class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

    def perform_create(self, serializer):
        sender_user = self.request.user
        recipient_user = serializer.validated_data['recipient_user']
        name = f'channel_{random.randint(1000, 9999)}'
        print(f'Creating channel: sender_user={sender_user}, recipient_user={recipient_user}, name={name}')  # Debugging
        serializer.save(sender_user=sender_user, recipient_user=recipient_user, name=name)

    def get_queryset(self):
        user = self.request.user
        return Channel.objects.filter(sender_user=user) | Channel.objects.filter(recipient_user=user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        channel = self.get_object()
        if request.user == channel.recipient_user:
            channel.accepted = True
            channel.save()
            return Response({'status': 'channel accepted'})
        else:
            return Response({'status': 'not allowed'}, status=403)




class SecretExchangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, channel_id):
        channel = Channel.objects.get(id=channel_id)
        if channel.accepted and (request.user == channel.sender_user or request.user == channel.recipient_user):
            secret_key = int.from_bytes(os.urandom(32), 'big')
            if request.user == channel.sender_user:
                channel.initial_sender_secret = pow(settings.BASE, secret_key, settings.MODULUS)
                channel.save()
                return Response({'secret_key': secret_key})
            elif request.user == channel.recipient_user:
                channel.initial_recipient_secret = pow(settings.BASE, secret_key, settings.MODULUS)
                channel.save()
                return Response({'secret_key': secret_key})
        else:
            return Response({'status': 'not allowed'}, status=403)

class KeyGenerationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, channel_id):
        channel = Channel.objects.get(id=channel_id)
        if channel.accepted and channel.initial_sender_secret and channel.initial_recipient_secret:
            secret_key = int.from_bytes(os.urandom(32), 'big')
            if request.user == channel.sender_user:
                key = pow(int(channel.initial_recipient_secret), secret_key, settings.MODULUS)
                return Response({'key': key})
            elif request.user == channel.recipient_user:
                key = pow(int(channel.initial_sender_secret), secret_key, settings.MODULUS)
                return Response({'key': key})
        else:
            return Response({'status': 'not allowed'}, status=403)
