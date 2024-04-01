from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)
    

class User(AbstractUser, PermissionsMixin):
    ROLES = (
        ('student', 'Student'),
        ('recruiter', 'Recruiter'),
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLES, default='student') 
    phone_numbers = models.CharField(max_length=100)
    username = models.CharField(max_length=150, unique=True)
    is_student = models.BooleanField('Is student', default=False)
    is_recruiter = models.BooleanField('Is recruiter', default=False)
    is_super_admin = models.BooleanField('Is super admin', default=False)
    is_banned = models.BooleanField(default=False, null=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager() 
    def __str__(self):
        return self.username
User = get_user_model()
  
class OnlineUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField()
    image = models.ImageField(upload_to="user")
    resume_link = models.URLField(blank=True, null=True)
    skills = models.ManyToManyField('Skill')
    educations = models.ManyToManyField('Education')

    def __str__(self):
        return self.user.username
class Skill(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
           return self.title
class Education(models.Model):
    year = models.IntegerField()
    department = models.CharField(max_length=100)
    university_name = models.CharField(max_length=100)
    def __str__(self):
           return self.university_name