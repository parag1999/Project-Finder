from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .serializers import (
    HackathonSerializer,
    HackathonTeamSerializer,
    HackathonTeamAddSerializer,
    HackathonTeamRequestDetailSerializer,
    HackathonTeamRequestCreateSerializer,
    HackathonTeamRequestUpdateSerializer,
    SkillSerializer,
    ProjectSerializer,
    ProjectTeamSerializer,
    ProjectTeamAddSerializer,
    ProjectTeamRequestDetailSerializer,
    ProjectTeamRequestCreateSerializer,
    ProjectTeamRequestUpdateSerializer,
    MentorRequestSerializer,
    MentorRequestUpdateSerializer,
)
from rest_framework import status
from .permissions import *
from django.http import HttpResponseRedirect
from .models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.serializers import ValidationError
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth import authenticate, login, logout
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from project_finder_web_app.serializers import UserCreateSerializer, UserLoginSerializer, UserDetailSerializer
from rest_framework.decorators import action


class UserDetailViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)


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
                return Response(serializer.data, status=HTTP_200_OK)
            else:
                raise ValidationError("Wrong Login Credentials")
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class HackathonViewSet(viewsets.ModelViewSet):
    serializer_class = HackathonSerializer
    queryset = Hackathon.objects.all()
    permission_classes = (IsTeacherOrIsAuthenticated,)
    # def get_serializer_class(self):
    #     if self.action == 'create' or self.action == 'update':
    #         return HackathonCreateSerializer
    #     return HackathonDetailSerializer


class HackathonTeamViewSet(viewsets.ModelViewSet):
    serializer_class = HackathonTeamSerializer
    queryset = HackathonTeam.objects.all()
    permission_classes = (IsTeacherOrIsAuthenticated,)

class HackathonTeamAddMember(UpdateAPIView):
    serializer_class = HackathonTeamAddSerializer
    queryset = HackathonTeam.objects.all()
    permission_classes = (IsAuthenticated,)


class HackathonTeamRequestList(ListAPIView):
    serializer_class = HackathonTeamRequestDetailSerializer
    queryset = HackathonTeamRequest.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        team = self.kwargs['team']
        hackathonteamrequest = HackathonTeamRequest.objects.filter(team__name=team)
        return hackathonteamrequest


class HackathonTeamRequestCreate(ListCreateAPIView):
    serializer_class = HackathonTeamRequestCreateSerializer
    queryset = HackathonTeamRequest.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class HackathonTeamRequestUpdate(UpdateAPIView):
    serializer_class = HackathonTeamRequestUpdateSerializer
    queryset = HackathonTeamRequest.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_fields = {'team', 'sender'}

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = []
        for field in self.lookup_fields:
            if self.kwargs[field]:
                filter.append(self.kwargs[field])
        obj = HackathonTeamRequest.objects.filter(team__name=filter[0], sender__email__iexact=filter[1]).first()
        self.check_object_permissions(self.request, obj)
        return obj


class HackathonTeamRequestDetail(ListAPIView):
    serializer_class = HackathonTeamRequestDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        team = self.kwargs['team']
        sender = self.kwargs['sender']
        queryset = HackathonTeamRequest.objects.filter(team__name=team, sender__email__iexact=sender)
        return queryset


class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
    # lookup_field = 'skill'
    permission_classes = (IsTeacher,)


class DeleteSkill(DestroyAPIView):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
    lookup_field = 'skill'
    permission_classes = (IsTeacher,)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = (IsStudent,)


class ProjectTeamViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectTeamSerializer
    queryset = ProjectTeam.objects.all()
    permission_classes = (IsStudent,)


class ProjectTeamAddMember(UpdateAPIView):
    serializer_class = ProjectTeamAddSerializer
    queryset = ProjectTeam.objects.all()
    permission_classes = (IsAuthenticated,)


class ProjectTeamRequestList(ListAPIView):
    serializer_class = ProjectTeamRequestDetailSerializer
    queryset = ProjectTeamRequest.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        team = self.kwargs['team']
        hackathonteamrequest = ProjectTeamRequest.objects.filter(team__name=team)
        return hackathonteamrequest


class ProjectTeamRequestCreate(ListCreateAPIView):
    serializer_class = ProjectTeamRequestCreateSerializer
    queryset = ProjectTeamRequest.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProjectTeamRequestUpdate(UpdateAPIView):
    serializer_class = ProjectTeamRequestUpdateSerializer
    queryset = ProjectTeamRequest.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_fields = {'team', 'sender'}

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = []
        for field in self.lookup_fields:
            if self.kwargs[field]:
                filter.append(self.kwargs[field])
        obj = ProjectTeamRequest.objects.filter(team__name=filter[0],
                                                sender__email__iexact=filter[1]).first()  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class ProjectTeamRequestDetail(ListAPIView):
    serializer_class = ProjectTeamRequestDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        team = self.kwargs['team']
        sender = self.kwargs['sender']
        queryset = ProjectTeamRequest.objects.filter(team__name=team, sender__email__iexact=sender)
        return queryset


class MentorRequestCreate(CreateAPIView):
    serializer_class = MentorRequestSerializer
    permission_classes = (IsNotMentor,)

# class MentorRequestSentList(ListAPIView):
#     serializer_class = MentorRequestSerializer
#     permission_classes = (IsAuthenticated,)

#     def get_queryset(self):
#         sender = request.User
#         queryset = ProjectTeamRequest.objects.filter(team__name=team, sender__email__iexact=sender)
#         return queryset

@api_view(["GET"])
@login_required()
def mentor_request_sent(request):
    """ For user """
    if request.method == "GET":
        sender = User.objects.filter(id=request.user.id)
        print(sender)
        mentor_request = MentorRequest.objects.filter(sender__in = sender)
        serializer = MentorRequestSerializer(mentor_request,many = True, context={'request': request}) 
        return Response(serializer.data)

@api_view(["GET"])
@login_required()
def mentor_request_received(request):
    """ For user """
    if request.method == "GET":
        receiver = User.objects.filter(id=request.user.id)
        print(receiver)
        mentor_request = MentorRequest.objects.filter(receiver__in = receiver)
        serializer = MentorRequestSerializer(mentor_request,many = True, context={'request': request}) 
        return Response(serializer.data)

    
class MentorRequestUpdate(UpdateAPIView):
    serializer_class = MentorRequestUpdateSerializer
    permission_classes = (IsMentor,)
    queryset = MentorRequest.objects.all()
    def get_object(self):
        pk_id = self.kwargs['pk']
        queryset = MentorRequest.objects.get(id=pk_id)
        return queryset

@api_view(["GET"])
@login_required()
def mentor_list(request):
    """ For user """
    if request.method == "GET":
        sender = User.objects.filter(id=request.user.id)
        print(sender)
        mentor_request = MentorRequest.objects.filter(sender__in = sender,status = 'A')
        serializer = MentorRequestSerializer(mentor_request,many = True, context={'request': request}) 
        return Response(serializer.data)

@api_view(["GET"])
@login_required()
def mentee_list(request):
    """ For user """
    if request.method == "GET":
        receiver = User.objects.filter(id=request.user.id)
        print(receiver)
        mentor_request = MentorRequest.objects.filter(receiver__in = receiver,status = 'A')
        serializer = MentorRequestSerializer(mentor_request,many = True, context={'request': request}) 
        return Response(serializer.data)
