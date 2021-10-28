from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        if other_fields.get('is_active') is not True:
            raise ValueError(
                'Superuser must be assigned to is_active=True.')

        return self.create_user(email, password, **other_fields)

class User(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(_('Email Address'), max_length=255, unique=True)
    first_name = models.CharField(_('First Name'), max_length=255, blank=True, null=True)
    last_name = models.CharField(_('Last Name'), max_length=255, blank=True, null=True)

    is_active = models.BooleanField(_('Active'), default=False)
    is_staff = models.BooleanField(_('Staff'), default=False)
    is_artist = models.BooleanField(_('Artist'), default=False)
    date_joined = models.DateTimeField(_('Created On'), default=timezone.now)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELD = []

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)
    
    def get_short_name(self):
        return self.first_name
    
