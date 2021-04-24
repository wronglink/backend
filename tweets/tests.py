from django.contrib.auth.models import User
from django.test import TestCase, Client

from tweets.models import Tweet
from users.models import Followings


class GetTweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Rick')
        self.tweet = Tweet.objects.create(text='Morty!', author=self.user)

    def test_get_tweet_by_id_correct_200(self):
        response = self.client.get(f'/v1/tweets/{self.tweet.id}/')
        self.assertEqual(response.status_code, 200)
        tweet = response.json()
        self.assertEqual(tweet['author']['username'], self.user.username)
        self.assertEqual(tweet['id'], self.tweet.id)
        self.assertEqual(tweet['text'], self.tweet.text)
        self.assertEqual(tweet['photo'], self.tweet.photo)

    def test_get_tweet_by_id_incorrect_404(self):
        self.assertEqual(self.client.get(f'/v1/tweets/666/').status_code, 404)


class GetTweetsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='Rick')
        self.user2 = User.objects.create(username='Morty')
        self.tweet11 = Tweet.objects.create(text='Morty!', author=self.user1)
        self.tweet21 = Tweet.objects.create(text='Rick!', author=self.user2)
        self.tweet22 = Tweet.objects.create(text='We are the champions!', author=self.user2)

    def test_get_user1_tweets(self):
        response = self.client.get(f'/v1/users/{self.user1.username}/tweets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json()['results'][0]['text'], self.tweet11.text)

    def test_get_user2_tweets(self):
        response = self.client.get(f'/v1/users/{self.user2.username}/tweets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)
        self.assertEqual(response.json()['results'][0]['text'], self.tweet22.text)
        self.assertEqual(response.json()['results'][1]['text'], self.tweet21.text)


class CreateTweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Jimmy')

    def test_create_by_anonymous_rejected(self):
        response = self.client.post(f'/v1/tweets/', {'text': 'Hello!'})
        self.assertEqual(response.status_code, 403)

    def test_create_by_user_correct(self):
        logined_client = Client()
        logined_client.force_login(self.user)
        response = logined_client.post(f'/v1/tweets/', {'text': 'Hello!'})
        self.assertEqual(response.status_code, 201)
        tweet_id = response.json()['id']
        self.assertEqual(self.client.get(f'/v1/tweets/{tweet_id}/').status_code, 200)


class FeedTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='Kevin')
        self.user2 = User.objects.create(username='Ricardo')
        self.user3 = User.objects.create(username='Christian')
        self.tweet11 = Tweet.objects.create(text='I am Kevin', author=self.user1)
        self.tweet12 = Tweet.objects.create(text='K-E-V-I-N!', author=self.user1)
        self.tweet21 = Tweet.objects.create(text='I am Ricardo', author=self.user2)
        self.tweet31 = Tweet.objects.create(text='I am Christian', author=self.user3)
        Followings.objects.create(follower=self.user2, follows=self.user3)
        Followings.objects.create(follower=self.user3, follows=self.user1)
        Followings.objects.create(follower=self.user3, follows=self.user2)

    def test_user1_feed_is_empty_if_not_following(self):
        self.client.force_login(self.user1)
        response = self.client.get(f'/v1/feed/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)
        self.assertEqual(response.json()['results'], [])

    def test_user3_feed_if_subscribed(self):
        self.client.force_login(self.user2)
        response = self.client.get(f'/v1/feed/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json()['results'][0]['id'], self.tweet31.id)

    def test_user2_feed_if_subscribed_several_users(self):
        self.client.force_login(self.user3)
        response = self.client.get(f'/v1/feed/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 3)
        self.assertEqual(
            [r['id'] for r in response.json()['results']],
            [self.tweet21.id, self.tweet12.id, self.tweet11.id],
        )
