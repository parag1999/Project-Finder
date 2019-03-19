from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import url
from project_finder_web_app import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register("hackathon", views.HackathonViewSet)
router.register("hackathonteam", views.HackathonTeamViewSet)
router.register("skill", views.SkillViewSet)
router.register("project", views.ProjectViewSet)
router.register("projectteam", views.ProjectTeamViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
    path('register/', csrf_exempt(views.UserCreateAPIView.as_view()), name='register'),
    path('detail/', views.UserDetailViewSet.as_view({'get': 'list'}), name='detail'),
    path('detail/<int:pk>',
         views.UserDetailViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='detail'),
    path('logout/', csrf_exempt(views.UserLogoutAPIView.as_view()), name='logout'),
    path('hackathon_team_addmember/<int:pk>', views.HackathonTeamAddMember.as_view(), name='hackathon_team_addmember'),
    path('hackathon_team_request_list/<str:team>',
         views.HackathonTeamRequestList.as_view(), name='hackathon_team_request_list'),
    path('hackathon_team_request_update/<str:team>/<str:sender>',
         views.HackathonTeamRequestUpdate.as_view(), name='hackathon_team_request_update'),
    path('hackathon_team_request_detail/<str:team>/<str:sender>',
         views.HackathonTeamRequestDetail.as_view(), name='hackathon_team_request_detail'),
    path('hackathon_team_request_create/',
         views.HackathonTeamRequestCreate.as_view(), name='hackathon_team_request_create'),
    path('delete_skills/<str:skill>', views.DeleteSkill.as_view(), name='delete_skills'),
    path('project_team_addmember/<int:pk>', views.ProjectTeamAddMember.as_view(), name='project_team_detail'),
    path('project_team_request_list/<str:team>',
         views.ProjectTeamRequestList.as_view(), name='project_team_request_list'),
    path('project_team_request_update/<str:team>/<str:sender>',
         views.ProjectTeamRequestUpdate.as_view(), name='project_team_request_update'),
    path('project_team_request_detail/<str:team>/<str:sender>',
         views.ProjectTeamRequestDetail.as_view(), name='project_team_request_detail'),
    path('project_team_request_create/', views.ProjectTeamRequestCreate.as_view(), name='project_team_request_create'),
    # path('hackathon_list/', views.HackathonList.as_view(), name='hackathon_list'),
    # path('hackathon_create/', views.HackathonCreate.as_view(), name='hackathon_create'),
    # path('hackathon_detail/<int:pk>', views.HackathonDetail.as_view(), name='hackathon_detail'),
    # path('hackathon_team_list/', views.HackathonTeamList.as_view(), name='hackathon_team_list'),
    # path('hackathon_team_create/', views.HackathonTeamCreate.as_view(), name='hackahon_team_create'),
    # path('hackathon_team_detail/<int:pk>', views.HackathonTeamDetail.as_view(), name='hackathon_team_detail'),
    # path('hackathon_team_update/<int:pk>', views.HackathonTeamUpdate.as_view(), name='hackathon_team_detail'),

    # path('add_skills/',
    #      views.AddSkill.as_view({'get': 'list', 'post': 'create'}), name='add_skills'),
    # path('project_list/', views.ProjectList.as_view(), name='project_list'),
    # path('project_create/', views.ProjectCreate.as_view(), name='project_create'),
    # path('project_detail/<int:pk>', views.ProjectDetail.as_view(), name='project_detail'),
    # path('project_team_list/', views.ProjectTeamList.as_view(), name='project_team_list'),
    # path('project_team_create/', views.ProjectTeamCreate.as_view(), name='hackahon_team_create'),
    # path('project_team_detail/<int:pk>', views.ProjectTeamDetail.as_view(), name='project_team_detail'),
    # path('project_team_update/<int:pk>', views.ProjectTeamUpdate.as_view(), name='project_team_detail'),

    # path('project_list/', views.ProjectList.as_view(), name='project_list'),
    # path('project_create/', views.ProjectCreate.as_view(), name='project_create'),
    # path('project_detail/<int:pk>', views.ProjectDetail.as_view(), name='project_detail'),
    # path('project_team_list/', views.ProjectTeamList.as_view(), name='project_team_list'),
    # path('project_team_create/', views.ProjectTeamCreate.as_view(), name='hackahon_team_create'),
    # path('project_team_detail/<int:pk>', views.ProjectTeamDetail.as_view(), name='project_team_detail'),
    # path('project_team_request_list/', views.ProjectTeamRequestList.as_view(), name='project_team_request_list'),
    # path('project_team_request_create/',
    # views.ProjectTeamRequestCreate.as_view(), name='project_team_request_create'),
]
