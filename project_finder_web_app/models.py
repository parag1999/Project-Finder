from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Skill(models.Model):
    skill = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.skill


class User(AbstractUser):
    email = models.EmailField(unique=True)
    sap_id = models.CharField(max_length=15, unique=True)
    mobile = models.CharField(max_length=10, unique=True)
    photo = models.FileField(upload_to='certain_location', blank=True, null=True)
    is_mentor = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)
    Github = models.URLField(null=True, blank=True)
    LinkedIN = models.URLField(null=True, blank=True)
    years = (
        ('FE', 'First Year'),
        ('SE', 'Second Year'),
        ('TE', 'Third Year'),
        ('BE', 'Fourth Year'),
    )
    year = models.CharField(max_length=2, choices=years, default='FE')
    skill_1 = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name='skill_1')
    skill_2 = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name='skill_2')
    skill_3 = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name='skill_3')
    interest_1 = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name='interest_1')
    interest_2 = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name='interest_2')
    interest_3 = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name='interest_3')

    def __str__(self):
        return self.email


class Project(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # creator = models.ForeignKey(User, on_delete=models.CASCADE)
    # skills_used = models.ManyToManyField(Skill)
    project_desc = models.TextField(max_length=500)
    link = models.URLField()

    def __str__(self):
        return self.name

    # def add_skills(self, skill):
        # self.skills_used.add(skill)
        # self.save()


class ProjectTeam(models.Model):
    name = models.CharField(max_length=50, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # leader = models.ForeignKey(User, on_delete=models.CASCADE)
    # current_members = models.ManyToManyField(User)
    vacancies = models.PositiveSmallIntegerField(default=3)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    # def add_member(self, member):
        # self.current_members.add(member)
        # self.save()


class ProjectTeamRequest(models.Model):
    # sender = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(ProjectTeam, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    create_date = models.DateField(default=timezone.now)
    status_choices = (
        ('A', 'Accepted'),
        ('P', 'Pending'),
        ('R', 'Rejected'),
    )
    status = models.CharField(max_length=1, choices=status_choices, default='P')

    def __str__(self):
        return self.sender.username + ' --> ' + self.team.name

    def accept(self):
        self.status = 'A'
        self.save()

    def reject(self):
        self.status = 'R'
        self.save()
