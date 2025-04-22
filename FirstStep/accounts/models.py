from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AccountManager(BaseUserManager):
    def create_user(self, email, username, firstname, lastname, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            firstname=firstname,
            lastname=lastname
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

# User model
class Account(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    profile_photo = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'firstname', 'lastname']

    def __str__(self):
        return self.email

class UserSettings(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    theme = models.CharField(max_length=100, default='light')
    language = models.CharField(max_length=100, default='en')
    notifications_enabled = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings for {self.user.username}"

class ActivityLog(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)
    description = models.TextField()
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.activity_type} by {self.user}"