from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User

from .serializers import (
    Register, 
    User1, 
    ChangePassword,
    PasswordResetRequest,
    PasswordResetConfirm
)

class RegisterView(generics.CreateAPIView):
   
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = Register
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens so user doesn't need to login again after signup
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': User1(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    #logout by blacklisting refresh token
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Frontend must send refresh token for logout
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(
                {'message': 'Logout successful'}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


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
                return Response(
                    {'error': 'Old password is incorrect'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response(
                {'message': 'Password changed successfully'}, 
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetRequest(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            
            # Verify user exists (already validated in serializer)
            try:
                user = User.objects.get(username=username)
                return Response(
                    {'message': 'User verified. You can now reset your password.'}, 
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response(
                    {'error': 'User not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirm(data=request.data)
        if serializer.is_valid():
            try:
                username = serializer.validated_data['username']
                user = User.objects.get(username=username)
                
                # Set new password
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                
                return Response(
                    {'message': 'Password reset successful'}, 
                    status=status.HTTP_200_OK
                )
                
            except User.DoesNotExist:
                return Response(
                    {'error': 'User not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({
        'message': 'Token is valid',
        'user': User1(request.user).data
    })