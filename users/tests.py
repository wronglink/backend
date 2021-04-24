from django.test import TestCase

from django.contrib.auth.models import User

from users.models import Followings


class GetUserTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="Leon")

    def test_get_existing_user_200(self):
        response = self.client.get(f'/v1/users/{self.user.username}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], self.user.username)

    def test_get_not_existing_user_404(self):
        self.assertEqual(self.client.get(f'/v1/users/incorrect/').status_code, 404)


class GetUsersTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username="Leon")
        self.user2 = User.objects.create(username="Kate")
        self.user3 = User.objects.create(username="John")

    def test_get_users_all(self):
        response = self.client.get(f'/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 3)
        self.assertEqual(
            [r['username'] for r in data['results']],
            [self.user3.username, self.user2.username, self.user1.username]
        )

    def test_get_users_page_1(self):
        response = self.client.get(f'/v1/users/', {'page': 1})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 3)
        self.assertEqual(
            [r['username'] for r in data['results']],
            [self.user3.username, self.user2.username, self.user1.username]
        )

    def test_get_users_page_2(self):
        self.assertEqual(self.client.get(f'/v1/users/', {'page': 2}).status_code, 404)


class PutFollowTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username="Leon")
        self.user2 = User.objects.create(username="Kate")

    def test_simple_add_follow(self):
        self.assertEqual(Followings.objects.count(), 0)
        self.client.force_login(self.user1)
        response = self.client.put(f'/v1/follow/{self.user2.username}/')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Followings.objects.count(), 1)

    def test_simple_delete_follow(self):
        self.assertEqual(Followings.objects.count(), 0)
        self.client.force_login(self.user1)
        self.client.put(f'/v1/follow/{self.user2.username}/')
        self.assertEqual(Followings.objects.count(), 1)
        response = self.client.delete(f'/v1/follow/{self.user2.username}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Followings.objects.count(), 0)

    def test_add_follow_twice_without_errors(self):
        self.assertEqual(Followings.objects.count(), 0)
        self.client.force_login(self.user1)
        self.assertEqual(self.client.put(f'/v1/follow/{self.user2.username}/').status_code, 201)
        self.assertEqual(Followings.objects.count(), 1)
        self.assertEqual(self.client.put(f'/v1/follow/{self.user2.username}/').status_code, 201)
        self.assertEqual(Followings.objects.count(), 1)


class GetUserFollowersAndFollowsTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username="Kelly")
        self.user2 = User.objects.create(username="Molly")
        self.user3 = User.objects.create(username="Sally")
        Followings.objects.create(follower=self.user1, follows=self.user2)
        Followings.objects.create(follower=self.user3, follows=self.user1)
        Followings.objects.create(follower=self.user3, follows=self.user2)

    def test_user3_followed_by_nothing(self):
        response = self.client.get(f'/v1/users/{self.user3.username}/followed/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

    def test_user2_follows_nothing(self):
        response = self.client.get(f'/v1/users/{self.user2.username}/follows/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

    def test_user1_followed_by_one(self):
        response = self.client.get(f'/v1/users/{self.user1.username}/followed/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json()['results'][0]['follower']['username'], self.user3.username)

    def test_user1_follows_one(self):
        response = self.client.get(f'/v1/users/{self.user1.username}/follows/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json()['results'][0]['follows']['username'], self.user2.username)

    def test_user2_followed_by_several(self):
        response = self.client.get(f'/v1/users/{self.user2.username}/followed/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

    def test_user3_follows_several(self):
        response = self.client.get(f'/v1/users/{self.user3.username}/follows/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)
