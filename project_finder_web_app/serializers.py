from .models import (
    Hackathon,
    HackathonTeam,
    HackathonTeamRequest,
    Skill,
    User,
    Project,
    ProjectTeam,
    ProjectTeamRequest,
    MentorRequest
)
from rest_framework import serializers
from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)



class UserCreateSerializer(ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'sap_id',
            'mobile',
            'photo',
            'is_mentor',
            'is_teacher',
            'bio',
            'year',
            'skills',
            'interests',
            'Github',
            'LinkedIN',
            'Behance',
            'StackOverFlow',
        ]

        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):

        sap_id = data['sap_id']
        user_qs = User.objects.filter(sap_id=sap_id)
        if user_qs.exists():
            raise ValidationError("This sap_id already registered.")
        return data

    def create(self, validated_data):
        password = validated_data['password']

        user_obj = User(
            username=validated_data["username"],
            sap_id=validated_data["sap_id"],
            mobile=validated_data["mobile"],
            email=validated_data["email"],
            bio=validated_data["bio"],
            photo=validated_data["photo"],
            is_mentor=validated_data["is_mentor"],
            is_teacher=validated_data["is_teacher"],
            year=validated_data["year"],
        )
        user_obj.set_password(password)
        user_obj.save()
        for i in range(len(validated_data["skills"])):
            user_obj.skills.add(validated_data["skills"][i])
        for i in range(len(validated_data["interests"])):
            user_obj.skills.add(validated_data["interests"][i])
        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    username = CharField()
    password = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        extra_kwargs = {"password": {"write_only": True}}


class HackathonSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.HyperlinkedRelatedField(view_name="detail", queryset=User.objects.all())

    class Meta:
        model = Hackathon
        fields = [
            'id',
            'name',
            'creator',
            'hackathon_desc',
            'link',
            'hackathon_date',
        ]


class HackathonTeamSerializer(serializers.ModelSerializer):
    current_member1 = serializers.HyperlinkedRelatedField(view_name="detail", queryset=User.objects.all())
    current_member2 = serializers.HyperlinkedRelatedField(view_name="detail", queryset=User.objects.all())
    current_member3 = serializers.HyperlinkedRelatedField(view_name="detail", queryset=User.objects.all())
    leader = serializers.HyperlinkedRelatedField(view_name="detail", queryset=User.objects.all())
    skills_required = serializers.HyperlinkedRelatedField(many=True, view_name='skill-detail', queryset=Skill.objects.all())

    class Meta:
        model = HackathonTeam
        fields = [
            'id',
            'name',
            'leader',
            'current_member1',
            'current_member2',
            'current_member3',
            'hackathon',
            'vacancies',
            'closed',
            'cut_off_date',
            'skills_required',
        ]


class HackathonTeamAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = HackathonTeam
        fields = [
            'id',
            'name',
            'leader',
            'current_member1',
            'current_member2',
            'current_member3',
            'hackathon',
            'vacancies',
            'closed',
            'cut_off_date',
            'skills_required',
        ]
        read_only_fields = ('name', 'leader', 'hackathon', 'cut_off_date', 'skills_required')

    def update(self, instance, validated_data):
        instance.current_member1 = validated_data['current_member1']
        instance.current_member2 = validated_data['current_member2']
        instance.current_member3 = validated_data['current_member3']
        instance.closed = validated_data['closed']
        instance.vacancies = validated_data['vacancies']
        instance.save()

        return instance


class HackathonTeamRequestDetailSerializer(serializers.ModelSerializer):
    sender = serializers.HyperlinkedRelatedField(view_name="detail", queryset=User.objects.all())
    team = serializers.HyperlinkedRelatedField(view_name="hackathonteam-detail", queryset=User.objects.all())
    skills = serializers.HyperlinkedRelatedField(many=True, view_name='skill-detail', queryset=Skill.objects.all())

    class Meta:
        model = HackathonTeamRequest
        fields = [
            'id',
            'sender',
            'team',
            'message',
            'skills',
            'create_date',
            'status',
        ]


class HackathonTeamRequestCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = HackathonTeamRequest
        fields = [
            'id',
            'sender',
            'team',
            'message',
            'skills',
            'create_date',
            'status',
        ]


class HackathonTeamRequestUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = HackathonTeamRequest
        fields = [
            'id',
            'sender',
            'team',
            'message',
            'skills',
            'create_date',
            'status',
        ]
        read_only_fields = ('sender', 'team', 'message', 'skills', 'create_date')

    def update(self, instance, validated_data):
        instance.status = validated_data['status']
        instance.save()

        return instance


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ['id', 'skill']


class ProjectSerializer(serializers.ModelSerializer):
    creator = serializers.HyperlinkedRelatedField(view_name="detail", queryset=User.objects.all())
    skills_used = serializers.HyperlinkedRelatedField(many=True, view_name='skill-detail', queryset=Skill.objects.all())

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'creator',
            'project_desc',
            'link',
            'skills_used',
        ]


class ProjectTeamSerializer(serializers.ModelSerializer):
    current_member1 = serializers.HyperlinkedRelatedField(view_name="detail", queryset=User.objects.all())
    current_member2 = serializers.HyperlinkedRelatedField(view_name="detail", queryset=User.objects.all())
    current_member3 = serializers.HyperlinkedRelatedField(view_name="detail", queryset=User.objects.all())
    leader = serializers.HyperlinkedRelatedField(view_name="detail", queryset=User.objects.all())

    class Meta:
        model = ProjectTeam
        fields = [
            'id',
            'name',
            'leader',
            'current_member1',
            'current_member2',
            'current_member3',
            'project',
            'vacancies',
            'closed',
        ]


class ProjectTeamAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectTeam
        fields = [
            'id',
            'name',
            'leader',
            'current_member1',
            'current_member2',
            'current_member3',
            'project',
            'vacancies',
            'closed',
        ]
        read_only_fields = ('name', 'leader', 'project',)

    def update(self, instance, validated_data):
        instance.current_member1 = validated_data['current_member1']
        instance.current_member2 = validated_data['current_member2']
        instance.current_member3 = validated_data['current_member3']
        instance.closed = validated_data['closed']
        instance.vacancies = validated_data['vacancies']
        instance.save()

        return instance


class ProjectTeamRequestDetailSerializer(serializers.ModelSerializer):
    sender = serializers.HyperlinkedRelatedField(view_name="detail", queryset=User.objects.all())
    team = serializers.HyperlinkedRelatedField(view_name="projectteam-detail", queryset=User.objects.all())
    skills = serializers.HyperlinkedRelatedField(many=True, view_name='skill-detail', queryset=Skill.objects.all())

    class Meta:
        model = ProjectTeamRequest
        fields = [
            'id',
            'sender',
            'team',
            'message',
            'skills',
            'create_date',
            'status',
        ]


class ProjectTeamRequestCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectTeamRequest
        fields = [
            'id',
            'sender',
            'team',
            'message',
            'skills',
            'create_date',
            'status',
        ]


class ProjectTeamRequestUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectTeamRequest
        fields = [
            'id',
            'sender',
            'team',
            'message',
            'skills',
            'create_date',
            'status',
        ]
        read_only_fields = ('sender', 'team', 'message', 'skills', 'create_date',)

    def update(self, instance, validated_data):
        instance.status = validated_data['status']
        instance.save()

        return instance


class MentorRequestSerializer(serializers.ModelSerializer):
    sender = serializers.HyperlinkedRelatedField(view_name="detail", queryset=User.objects.all())
    receiver = serializers.HyperlinkedRelatedField(view_name="detail", queryset=User.objects.all())
    class Meta:
        model = MentorRequest
        fields = "__all__" 


class MentorRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorRequest
        fields = "__all__"
        read_only_fields = ('sender', 'receiver',  'skills', 'created_on',)
    
    def update(self, instance, validated_data):
        instance.status = validated_data['status']
        instance.save()
        return instance    
class UserDetailSerializer(ModelSerializer):
    skills = serializers.HyperlinkedRelatedField(many=True, view_name='skill-detail', queryset=Skill.objects.all())
    interests = serializers.HyperlinkedRelatedField(many=True, view_name='skill-detail', queryset=Skill.objects.all())
    projects = ProjectSerializer(read_only=True, many=True,)
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'sap_id',
            'mobile',
            'photo',
            'is_mentor',
            'is_teacher',
            'bio',
            'year',
            'skills',
            'interests',
            'Github',
            'LinkedIN',
            'Behance',
            'StackOverFlow',
            'projects'
        ]
