from django.db import models

# Create your models here.
class Enquiry(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    contact=models.CharField(max_length=15)
    subject=models.CharField(max_length=200)
    message=models.TextField()
    enqdate=models.DateTimeField(auto_now_add=True)
    
class LoginInfo(models.Model):
    usertype=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    password=models.CharField( max_length=50)
    status=models.CharField(max_length=100,default="active")
    
class UserInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=59, unique=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile = models.ImageField(upload_to='profile/', blank=True, null=True)
    login = models.OneToOneField(LoginInfo, on_delete=models.CASCADE, null=True, blank=True)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.name
