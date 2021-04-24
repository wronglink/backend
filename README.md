## Day 1
#### 1. Create django's empty project

   1.1. Install dependencies
   ```bash
   pip install "django>=3.1"
   pip install "djangorestframework>=3.12"
   ```
   1.2. Init project
   ```bash
   django-admin startproject twitter .
   ```
   1.3. Run server
   ```bash
   python manage.py runserver
   ```
   1.4. Check http://127.0.0.1:8000/

#### 2. Django's admin interface
   
   2.1. Init app with users
   ```bash
   django-admin startapp users
   ```
   2.2. Migrate DB
   ```bash
   python manage.py migrate
   ```
   2.3. Create admin with password `qwerty` for testing
   ```bash
   python manage.py createsuperuser --email admin@example.com --username admin
   ```
   2.4. Run server `python manage.py runserver` and go to http://127.0.0.1:8000/admin

#### 2.5 Make API work in swagger-ui (aka CORS):
   2.5.1 Install django app
   ```
   pip install django-cors-headers
   ```
   2.5.2. Add to settings:
   ```
   INSTALLED_APPS = [
     'django.contrib.messages',
     'django.contrib.staticfiles',
     'rest_framework',
   + 'corsheaders',
     'django_filters',
     'tweets.apps.TweetsConfig',
     ...

   MIDDLEWARE = [
     'django.middleware.security.SecurityMiddleware',
     'django.contrib.sessions.middleware.SessionMiddleware',
   + 'corsheaders.middleware.CorsMiddleware',
     'django.middleware.common.CommonMiddleware',
     'django.middleware.csrf.CsrfViewMiddleware',
     ...

   +CORS_ALLOW_ALL_ORIGINS = True
   ```

#### 3. Simple users-API
   
   3.1. Create file `users/serializers.py`
   
   3.2. Edit file `users/views.py`
   
   3.3. Edit file `twitter/urls.py`
   
   3.4. Edit file `twitter/settings.py`
   
   3.5. Run server `python manage.py runserver`
   
   3.6. Check API works correctly
   
      3.6.1. By `curl`:
      ```bash
      curl -H 'Accept: application/json; indent=4' -u admin:qwerty http://127.0.0.1:8000/users/
      ```
      3.6.2. In browser http://127.0.0.1:8000

#### 4. Simple tweets-API
   
   4.1. Init app with tweets
   ```bash
   django-admin startapp tweets
   ```
   4.2. Edit file `tweets/models.py`
   
   4.3. Create file `tweets/serializers.py`
   
   4.4. Edit file `tweets/views.py`
   
   4.5. Edit file `twitter/urls.py`
   
   4.6. Edit file `twitter/settings.py`
   
   4.7. Make migration and migrate
   ```bash
   python manage.py makemigrations tweets
   python manage.py migrate
   ```
   
   4.8. Run server `python manage.py runserver`

#### 5. Filters
   
   5.1. Install dependency `pip install "django-filter>=2.4.0"`

   5.2. Edit `tweets/views.py` add `filterset_class = TweetFilter`

## Day 2

#### 1. CRUD tweets & permissions
   
   1.1. Create `tweets/permissions.py` with `IsAuthorOrReadOnly`

   1.2. Edit `tweets/views.py`.
        Change `TweetsViewSet`: base - `ModelViewSet`, add `permission_classes`, add `get_queryset`

   1.3. Add and register `UserTweetsViewSet` and `FeedViewSet`

#### 2. followers

   2.1. Declare model `Followings`

   2.2. Generate migration and migrate
   ```bash
   python manage.py makemigrations users
   python manage.py migrate
   ```

   2.3. Declared followings serializers `FollowsSerializer` and `FollowedSerializer`

   2.4. Add view-sets `UserFollowedViewSet` and `UserFollowsViewSet` and register thems in `urls.py`
