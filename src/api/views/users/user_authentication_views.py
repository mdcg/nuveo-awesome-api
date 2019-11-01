from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.user_serializers import UserSerializer
from rest_framework_jwt.settings import api_settings


class SignUpView(APIView):
    def post(self, request):
        user_to_register = UserSerializer(data=request.data)

        if user_to_register.is_valid():
            user = user_to_register.save()

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            serialized_user_information = UserSerializer(user)

            payload = {
                'status': 'success',
                'data': {
                    'user': {
                        **serialized_user_information.data,
                        'token': token,
                    },
                },
            }
            return Response(payload, status=status.HTTP_201_CREATED)

        payload = {
            'status': 'fail',
            'data': user_to_register.errors,
        }
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if not username or not password:
            payload = {
                'status': 'fail',
                'data': {
                    'username': ['This field is required.'],
                    'password': ['This field is required.'],
                },
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            serialized_user_information = UserSerializer(user)

            payload = {
                'status': 'success',
                'data': {
                    'user': {
                        **serialized_user_information.data,
                        'token': token,
                    },
                },
            }
            return Response(payload, status=status.HTTP_200_OK)

        payload = {
            'status': 'fail',
            'data': None,
        }
        return Response(payload, status=status.HTTP_403_FORBIDDEN)
