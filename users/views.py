from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate


from .models import CustomUser, Profile
from .serializers import (
    CustomTokenRefreshSerializer, 
    UserLoginSerializer, 
    UserRegistrationSerializer,
    ProfileSerializer,
    UserListSerializer,
    PasswordChangeSerializer
)



class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    queryset = CustomUser.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        
        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'username': serializer.data['username'],
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh']
            }

        return Response(response, status=status_code)


class UserRegistrationView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]


class PasswordUpdateView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]


    def perform_update(self, serializer):
        # Hash password but passwords are not required
        if ('password' in self.request.data):
            password = make_password(self.request.data['password'])
            serializer.save(password=password)


class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer



@permission_classes([IsAdminUser])
@api_view(['POST'])
def approve_user(request, pk):
    user = request.user
    user = CustomUser.objects.get(id=pk)
    user.is_active = True
    user.save()
    
    return Response('User approved')


@permission_classes([IsAdminUser])
@api_view(['POST'])
def reject_user(request, pk):
    user = request.user
    user = CustomUser.objects.get(id=pk)
    user.is_active = False
    user.save()
    
    return Response('User rejected')


@permission_classes([IsAdminUser])
@api_view(["POST"])
def user_logout_view(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(username = username, password = password)

    if user is not None:
        return Response('User successfully logged out', status=status.HTTP_200_OK)
    else:
        return Response("Username or Password is incorrect.", status=status.HTTP_400_BAD_REQUEST)

