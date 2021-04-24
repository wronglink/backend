"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_extensions.routers import ExtendedSimpleRouter

from twitter.routers import SwitchDetailRouter
from users.views import UsersViewSet, FollowingsViewSet
from tweets.views import TweetsViewSet, FeedViewSet, UserTweetsViewSet

switch_detail_router = SwitchDetailRouter()
switch_detail_router.register(r'follow', FollowingsViewSet)

router = ExtendedSimpleRouter()
router.register(r'users', UsersViewSet)\
    .register(r'tweets', UserTweetsViewSet, 'user-tweets', ['username'])
router.register(r'feed', FeedViewSet)
router.register(r'tweets', TweetsViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('v1/', include(switch_detail_router.urls)),
    path('v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
