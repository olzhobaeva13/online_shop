from django.shortcuts import render
from rest_framework import response
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import RegistrationSerializer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action

User = get_user_model()

class RegistrationAPIView(APIView):
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(operation_description='User regisrtation',
                         request_body=RegistrationSerializer,
                         methods=['post', ],
                         responses={200: 'user registered successfully', 400: 'bad request'})
    @action(detail=True, methods=['post', ], serializer_class=RegistrationSerializer)
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({'message': 'user with such username is already exists'},
                             status = status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({token: token.key}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(operation_description='User regisrtation',
                         request_body=RegistrationSerializer,
                         methods=['post', ],
                         responses={200: 'user registered successfully', 400: 'bad request'})
    @action(detail=True, methods=['post', ], serializer_class=RegistrationSerializer)
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(operation_description='User regisrtation',
                         request_body=RegistrationSerializer,
                         methods=['post', ],
                         responses={200: 'user registered successfully', 400: 'bad request'})
    @action(detail=True, methods=['post', ], serializer_class=RegistrationSerializer)
    def post(self, request):
        user = request.user
        token = Token.objects.filter(user=user).first()
        token.delete()
        return Response({'success': True})