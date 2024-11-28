# main/api_views.py
#REST Api näkymä funktiot
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from .models import Post, Comment, Like, User
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, SignupSerializer
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
#jwt
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

'''
#Poistaa CSRF tarkistuksen testausta varten
#Viittaa ViewSetissä lisäämäällä --> authentication_classes = [CsrfExemptSessionAuthentication]
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # Ei tarkista CSRF-tokenia
'''

# jwt Login view, joka palauttaa JWT tokenit
class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)


# jwt Refresh token view
class MyTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)

#perus api näkymät
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        print("Received data:", self.request.data)  #  DEBUG Tulostaa saatu data
        post_id = self.request.data.get('post')
        print("Post ID:", post_id)  #  DEBUG Tulostaa post_id:n
        try:
            post = Post.objects.get(id=post_id)
            print("Post found:", post)  # DEBUG Tulosta löytyneen postin
            serializer.save(commenter=self.request.user, post=post)
        except Post.DoesNotExist:
            print(f"Post with id {post_id} does not exist.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        print("Received data:", self.request.data)  
        post_id = self.request.data.get('post')    #hakee Post avaimesta id arvon
        print("Post ID:", post_id)  # Tulostaa post_id:n
        try:
            post = Post.objects.get(id=post_id)   #hae Post taulusta objekti jonka id on sama kuin post_id
            print("Post found:", post)  # Tulostaa löytyneen postin
            serializer.save(liker=self.request.user, post=post)  #serializer tallettaa tykkääjän ja postauksen johon tykkäys liittyy
        except Post.DoesNotExist:
            print(f"Post with id {post_id} does not exist.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            # Adminit näkevät kaikki käyttäjät
            return User.objects.all()
        # Tavalliset käyttäjät näkevät vain omat tietonsa
        return User.objects.filter(id=user.id)
    
   
    def is_superuser(self, request):
        # Tarkistetaan, onko käyttäjä superuser
        is_superuser = request.user.is_superuser
        return Response({"is_superuser": is_superuser})


#Käyttäjä tiedot
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    """
    Palauttaa kirjautuneen käyttäjän profiilitiedot.
    """
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)    

'''
#csfr login
@api_view(['POST'])
def login_view(request):
    """
    Ohje.
    Käyttäjän kirjautuminen.
    Kirjoita käyttäjätunnus ja salasana POST-pyyntöön JSON-muodossa ja merkkijonot string tyyppinä. 
    Esim:

    {
    "username": "Käyttäjä",
    "password": "salasana"
    }
    
    """
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

'''

#jwt login
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Käyttäjän kirjautuminen ja JWT tokenin palauttaminen.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        # Kirjautuminen onnistui, luo JWT token
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# Tunnusten luonti API endpoint
@api_view(['POST'])
@permission_classes([AllowAny])    #ohitettu JWT tarkistus koska kyseessä on uuden käyttäjän luonti
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#jwt ei tarvitse mutta saa olla
@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

#tee csfr token haku kun suoritetaan POST ja DELETE pyyntöjä 'api/csfr' , jwt ei tarvita
def csrf_token_view(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

