# main/urls.py
#jwt importit start
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
#jwt import end


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
    #csfr
    path('api/', include(router.urls)),
    path('api/login/', login_view, name='api_login'),   #muutettu jwt auth
    path('api/logout/', logout_view, name='api_logout'),
    path('api/csrf/', csrf_token_view, name='csrf-token'),
    path('api/profile/', api_views.user_profile_view, name='user-profile'),
    path('api/signup/', api_views.signup, name='signedup'),

    #jwt 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #jwt

    #feed
    #path('', views.feed, name='feed'),
]

#ok