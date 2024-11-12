# main/urls.py

from rest_framework.routers import DefaultRouter
from .api_views import CommentViewSet, LikeViewSet,UserViewSet, login_view, logout_view ,PostViewSet
from django.urls import path, include
from . import api_views
from .api_views import csrf_token_view  #,PostCreateView

# REST API reititys
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'users', UserViewSet)
    
# URLS
urlpatterns = [
    # REST API reitit
    path('api/', include(router.urls)),
    path('api/login/', login_view, name='api_login'),
    path('api/logout/', logout_view, name='api_logout'),
    path('api/csrf/', csrf_token_view, name='csrf-token'),
    path('api/profile/', api_views.user_profile_view, name='user-profile'),
    path('api/signup/', api_views.signup, name='signedup'),
    #feed
    #path('', views.feed, name='feed'),
]

#ok