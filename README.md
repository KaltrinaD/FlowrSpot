# FlowrSpot

This is an API in Python for a mobile app called FlowrSpot. The app is used for flower spotting while hiking, traveling, etc. 
Users can check out different flowers, their details, nd sightings as well as add their sightings. 
The backend API and mobile app communicate via JSON. The database is MySQL.

Project Installation & Setup


Create New Project on PyCharm

pip install django

django-admin startproject core
django-admin startapp users


Application definition
settings.py
INSTALLED_APPS = [
	...
    'users',
    'rest_framework',
    'corsheaders',
    'django_seed'
]

install corsheaders python pip install django-cors-header

settings.py
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
     ...
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
]



CORS_ORIGIN_ALLOW_ALL = True  #in production only whitelisted domains
CORS_ALLOW_CREDENTIALS = True


Models/Serializers

pip install mysqlclient

Create models.py file containing custom User model class, Flower Model, Sighting Model, Like Model
python manage.py

Create serializers serializers.py

python manage.py makemigrations
python manage.py migrate

settings.py
AUTH_USER_MODEL = 'users.User'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',

    }
}

Route and API views:


users/views.py:

RegisterView  - used to register a client, accepts only POST requests (required fields: email, password, name)
LoginView -used to login a client, accepts only POST requests (required fields: email, password)
LogoutView- used to logout a client, accepts only POST requests
FlowerView- returns a list of all flowers
FlowerViewByIdView- returns a list of sighitngs for a particular flower  
SightingView- GET all sightings, POST a sighting
SightingByIdView -GET/DELETE a sighting by ID
LikesSightingView -GET/POST a sighting
LikesSightingLViewById - GET/PATCH a like

users/urls.py:

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('flowers', FlowerView.as_view(),name="flowers_all"),
    path('flowers/<int:id>/', FlowerViewByIdView.as_view(),name="flowers_all"),
    path('sightings', SightingView.as_view(), name="sightings_all"),
    path('sightings/<int:id>/', SightingByIdView.as_view(), name="sightings_byId"),
    path('likes', LikesSightingView.as_view(), name="likes_all"),
    path('likes/<int:id>/', LikesSightingLViewById.as_view(), name="likes_byId"),

]



Authentication

python install djangorestframework-simplejwt
python pip install PyJWT

pip install djangorestframework_simplejwt

settings.py:

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
}


SIMPLE_JWT = {
'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
'ALGORITHM': 'HS256',
'AUTH_HEADER_TYPES': ('Bearer',),
'BLACKLIST_AFTER_ROTATION': True,
'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
'SLIDING_TOKEN_LIFETIME': timedelta(days=10),
'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=20)
}


urls.py

from django.urls import path
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/token', TokenObtainPairPatchedView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name="token_refresh"),
]


Example Code

Route and API views:

views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
		
		
urls.py

from django.urls import path
from myapi.core import views

urlpatterns = [
    path('register', RegisterView.as_view()),
    ...
]


Usage:

HTTPie to consume the API endpoints via the terminal /DRF web interface

Authenticate and obtain the token. 

http post http://127.0.0.1:8000/api/token/ username123@123.com password=123

Response body is the two tokens:

{
    "access": "eyJ0eXAixxxxx.xxxxxx.xxxxxx",
    "refresh": "eyJ0eXAxxxxxxxxxxxxx.xxxxxxxxxxxxxxx.xxxxxxxxxxxxx"
}

Refresh Token
To get a new access token,use the refresh token endpoint /api/token/refresh/ posting the refresh token:

http post http://127.0.0.1:8000/api/token/refresh/ refresh=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlb

