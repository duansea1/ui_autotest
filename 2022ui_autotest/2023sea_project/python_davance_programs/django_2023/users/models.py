from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class UserModel(User):
    mobile = models.CharField(max_length=11, null=True, blank=True)
    username = models.CharField()
