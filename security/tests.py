from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Channel


class SecureKeyExchangeTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.client.login(username='user1', password='password123')

    def test_create_channel(self):
        response = self.client.post('/api/channels/', {'recipient_user': self.user2.id})
        print(response.content) 
        print(response.status_code) 
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Channel.objects.count(), 1)

    def test_accept_channel(self):
        channel = Channel.objects.create(sender_user=self.user1, recipient_user=self.user2, name='test_channel')
        self.client.login(username='user2', password='password123')
        response = self.client.post(f'/api/channels/{channel.id}/accept/')
        self.assertEqual(response.status_code, 200)
        channel.refresh_from_db()
        self.assertTrue(channel.accepted)
    
    def test_secret_exchange(self):
        channel = Channel.objects.create(sender_user=self.user1, recipient_user=self.user2, name='test_channel', accepted=True)
        response = self.client.post(f'/api/secret_exchange/{channel.id}/')
        self.assertEqual(response.status_code, 200)
        channel.refresh_from_db()
        self.assertIsNotNone(channel.initial_sender_secret)
    
    def test_key_generation(self):
        channel = Channel.objects.create(sender_user=self.user1, recipient_user=self.user2, name='test_channel', accepted=True, initial_sender_secret=123456, initial_recipient_secret=654321)
        response = self.client.post(f'/api/key_generation/{channel.id}/')
        self.assertEqual(response.status_code, 200)
