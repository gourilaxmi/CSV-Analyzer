from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate

from .serializers import (
    Register, 
    User1, 
    ChangePassword,
    PasswordResetRequest,
    PasswordResetConfirm,
    Login
)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = Register
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': User1(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = Login(data=request.data)
        if serializer.is_valid():
            login_id = serializer.validated_data['login_id']
            password = serializer.validated_data['password']

            try:
                user_obj = User.objects.get(Q(username=login_id) | Q(email=login_id))
            except User.DoesNotExist:
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            user = authenticate(username=user_obj.username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': User1(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    },
                    'message': 'Login successful'
                }, status=status.HTTP_200_OK)
            
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = User1
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePassword(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetRequest(data=request.data)
        if serializer.is_valid():
            # Simply confirms the user exists before showing the reset modal
            return Response({'message': 'User verified. You can now reset your password.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirm(data=request.data)
        if serializer.is_valid():
            login_id = serializer.validated_data['login_id']
            try:
                # Find user by username or email
                user = User.objects.get(Q(username=login_id) | Q(email=login_id))
                
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                
                return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({
        'message': 'Token is valid',
        'user': User1(request.user).data
    })