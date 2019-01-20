from django.http import HttpResponseRedirect
from .models import User
from rest_framework import viewsets
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)
from project_finder_web_app.serializers import UserCreateSerializer, UserLoginSerializer, UserDetailSerializer


class UserDetailViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(
                username=serializer.data.get("username"),
                password=serializer.data.get("password"),
            )
            if user:
                login(request, user)
# return HttpResponseRedirect(redirect_to="/menu_item/")
                return Response(serializer.data, status=HTTP_200_OK)
            else:
                raise ValidationError("Wrong Login Credentials")
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return HttpResponseRedirect(redirect_to="/login/")
