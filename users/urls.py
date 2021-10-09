from django.contrib import admin
from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, FlowerView, SightingView, SightingByIdView, \
     FlowerViewByIdView, LikesSightingLViewById, LikesSightingView


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




