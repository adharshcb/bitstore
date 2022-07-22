from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from requests import request
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('Email required')
        
        if not username:
            raise ValueError('Username required')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,first_name,last_name,username,email,password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_superadmin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)
    vendor_store = models.CharField(max_length=250,null=True,blank=True)
    

    #required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    vendor_req_status = models.BooleanField(default=False)
    vendor_req_rejection_status = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    is_mail_manager = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = MyAccountManager()

    def fullname(self):
        return self.first_name +" "+ self.last_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True

    def userprofile(self):
        return UserProfile.objects.get(user=self)



class UserProfile(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=100,blank=True)
    address_line_2 = models.CharField(max_length=100,blank=True)
    profile_image = models.ImageField(upload_to='user/profile_images/', blank = True)
    city = models.CharField(blank=True,max_length=30)
    state = models.CharField(blank=True,max_length=30)
    country = models.CharField(blank=True,max_length=30)

    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f'{self.address_line_1}, {self.address_line_2}'
