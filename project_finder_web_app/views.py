from .models import Hackathon, HackathonTeam, HackathonTeamRequest, Project, ProjectTeam, ProjectTeamRequest, Skill
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import (
    HackathonSerializer,
    # HackathonCreateSerializer,
    # HackathonDetailSerializer,
    HackathonTeamSerializer,
    # HackathonTeamCreateSerializer,
    # HackathonTeamDetailSerializer,
    HackathonTeamAddSerializer,
    HackathonTeamRequestDetailSerializer,
    HackathonTeamRequestCreateSerializer,
    HackathonTeamRequestUpdateSerializer,
    SkillSerializer,
    ProjectSerializer,
    # ProjectCreateSerializer,
    # ProjectDetailSerializer,
    ProjectTeamSerializer,
    # ProjectTeamCreateSerializer,
    # ProjectTeamDetailSerializer,
    ProjectTeamAddSerializer,
    ProjectTeamRequestDetailSerializer,
    ProjectTeamRequestCreateSerializer,
    ProjectTeamRequestUpdateSerializer,
    # ProjectSerializer,
    # ProjectDetailSerializer,
    # ProjectTeamSerializer,
    # ProjectTeamRequestSerializer,
)
from rest_framework import status
from .permissions import IsTeacher, IsReadOnly, IsOwnerOrReadOnly, IsStudent, IsTeacherOrIsAuthenticated
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


# class HackathonCreate(ListCreateAPIView):
#     serializer_class = HackathonCreateSerializer
#     queryset = Hackathon.objects.all()
#     permission_classes = (IsTeacher,)
#
#
# class HackathonList(ListAPIView):
#     serializer_class = HackathonDetailSerializer
#     queryset = Hackathon.objects.all()
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#
#
# class HackathonDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = HackathonDetailSerializer
#     queryset = Hackathon.objects.all()
#     permission_classes = (IsAuthenticated,)


class HackathonTeamViewSet(viewsets.ModelViewSet):
    serializer_class = HackathonTeamSerializer
    queryset = HackathonTeam.objects.all()
    permission_classes = (IsTeacherOrIsAuthenticated,)


# class HackathonTeamList(ListAPIView):
#     serializer_class = HackathonTeamDetailSerializer
#     queryset = HackathonTeam.objects.all()
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#
#
# class HackathonTeamCreate(CreateAPIView):
#     serializer_class = HackathonTeamCreateSerializer
#     queryset = HackathonTeam.objects.all()
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#
#
# class HackathonTeamDetail(RetrieveDestroyAPIView):
#     serializer_class = HackathonTeamDetailSerializer
#     queryset = HackathonTeam.objects.all()
#     permission_classes = (IsAuthenticated,)
#
#
# class HackathonTeamUpdate(UpdateAPIView):
#     serializer_class = HackathonTeamCreateSerializer
#     queryset = HackathonTeam.objects.all()
#     permission_classes = (IsAuthenticated,)


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

# class ProjectCreate(ListCreateAPIView):
#     serializer_class = ProjectCreateSerializer
#     queryset = Project.objects.all()
#     permission_classes = (IsAuthenticated,)
#
#
# class ProjectList(ListAPIView):
#     serializer_class = ProjectDetailSerializer
#     queryset = Project.objects.all()
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#
#
# class ProjectDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = ProjectDetailSerializer
#     queryset = Project.objects.all()
#     permission_classes = (IsAuthenticated,)


class ProjectTeamViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectTeamSerializer
    queryset = ProjectTeam.objects.all()
    permission_classes = (IsStudent,)


# class ProjectTeamList(ListAPIView):
#     serializer_class = ProjectTeamDetailSerializer
#     queryset = ProjectTeam.objects.all()
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#
#
# class ProjectTeamCreate(CreateAPIView):
#     serializer_class = ProjectTeamCreateSerializer
#     queryset = ProjectTeam.objects.all()
#     permission_classes = (IsStudent,)
#
#
# class ProjectTeamDetail(RetrieveDestroyAPIView):
#     serializer_class = ProjectTeamDetailSerializer
#     queryset = ProjectTeam.objects.all()
#     permission_classes = (IsAuthenticated,)
#
#
# class ProjectTeamUpdate(UpdateAPIView):
#     serializer_class = ProjectTeamCreateSerializer
#     queryset = ProjectTeam.objects.all()
#     permission_classes = (IsAuthenticated,)


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


# class ProjectList(ListAPIView):
#     serializer_class = ProjectSerializer
#     queryset = Project.objects.all()
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#
#
# class ProjectCreate(ListCreateAPIView):
#     serializer_class = ProjectSerializer
#     queryset = Project.objects.all()
#     permission_classes = (IsAuthenticated,)
#
#
# # Here the permissions are not working
# class ProjectDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = ProjectDetailSerializer
#     queryset = Project.objects.all()
#     permission_classes = (IsAuthenticated,)
#
#
# class ProjectTeamList(ListAPIView):
#     serializer_class = ProjectTeamSerializer
#     queryset = ProjectTeam.objects.all()
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#
#
# class ProjectTeamCreate(ListCreateAPIView):
#     serializer_class = ProjectTeamSerializer
#     queryset = ProjectTeam.objects.all()
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#
#
# class ProjectTeamDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = ProjectTeamSerializer
#     queryset = ProjectTeam.objects.all()
#     permission_classes = (IsAuthenticated,)
#
#
# class ProjectTeamRequestList(ListAPIView):
#     serializer_class = ProjectTeamRequestSerializer
#     queryset = HackathonTeamRequest.objects.all()
#     permission_classes = (IsAuthenticated,)
#
#
# class ProjectTeamRequestCreate(ListCreateAPIView):
#     serializer_class = ProjectTeamRequestSerializer
#     queryset = ProjectTeamRequest.objects.all()
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#
#
# class ProjectTeamRequestViewSet(viewsets.ModelViewSet):
#     serializer_class = ProjectTeamRequestSerializer
#     queryset = ProjectTeamRequest.objects.all()
#
#     @action(detail=True, methods=["put", "get"])
#     def accept(self, request, pk=None):
#         project_team_request = self.get_object()
#         project_team_request.accept()
#         return Response({"message": "Request accepted"})
#
#     @action(detail=True, methods=["put", "get"])
#     def reject(self, request, pk=None):
#         project_team_request = self.get_object()
#         project_team_request.reject()
#         return Response({"message": "Request rejected"})

#
# class HackathonTeamRequestViewSet(viewsets.ModelViewSet):
#     serializer_class = HackathonTeamRequestCreateSerializer
#     queryset = HackathonTeamRequest.objects.all()
#
#     @action(detail=False, methods=["put", "get"])
#     def status(self, request, pk=None):
#         hackathon_team_request = self.get_object()
#         print(hackathon_team_request.sender)
#         if hackathon_team_request.status == 'A':
#             hackathon_team_request.accept()
#             return Response({"message": "Request accepted"})
#         elif hackathon_team_request.status == 'R':
#             hackathon_team_request.reject()
#             return Response({"message": "Request rejected"})
#         else:
#             return Response({"message":"Request pending"})
    # @action(detail=True, methods=["put", "get"])
    # def reject(self, request, pk=None):
    #     hackathon_team_request = self.get_object()
    #     hackathon_team_request.reject()
    #     return Response({"message": "Request rejected"})

# @api_view(['GET','PUT'])
# def HackathonTeamRequestUpdate(request,team,sender):
#     try:
#         queryset = HackathonTeamRequest.objects.filter(team__name=team,sender__email__iexact=sender)
#     except HackathonTeamRequest.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = HackathonTeamRequestCreateSerializer(queryset,many=True)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         queryset = HackathonTeamRequest.objects.filter(team__name=team,sender__email__iexact=sender)
#         serializer = HackathonTeamRequestCreateSerializer(queryset,data=data,partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # serializer = HackathonTeamRequestSerializer(queryset)
    # return Response(serializer.data)
