import os
import random
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model

User  = settings.AUTH_USER_MODEL

#####################################Profile User#####################################
# create custom def to uplaod images
  #  here we will divide the image to name and ext
def change_name_img(filename):
  basname = os.path.basename(filename)
  name, ext = os.path.splitext(basname)
  return name, ext

  # here we save profile image for user in a custome folder
def upload_to(instance, filename):
  new_name = random.randint(1, 123456789)
  name, ext = change_name_img(filename)
  final_name = f'{new_name}{ext}'
  return f"profile_picture/{instance.iqama}/{final_name}"



class ProfileUser(models.Model):
  user      = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
  company   = models.CharField(max_length=50, null=True, blank=True)
  fullname  = models.CharField(max_length=30)
  iqama     = models.CharField(max_length=10)
  phone     = PhoneNumberField(region='SA',)
  email     = models.EmailField(max_length=150,)
  headline  = models.CharField(max_length=60, null= True, blank= True,help_text='Add a professional headline.')
  bio       = models.TextField(null= True, blank= True,help_text='Links and coupon codes are not permitted in this section.')
  photo     = models.ImageField(upload_to=upload_to, null=True, blank=True)

  def __str__(self):

      return self.email

  class Meta:
    verbose_name        = "Public Profile User"
    verbose_name_plural = "Puplic Profile Users"  



def get_user_to_public_profile(instance, sender, created, *args, **kwargs):
  """ we get or create user in public profile when it created in accounts app """
  if created:
    ProfileUser.objects.get_or_create(user=instance, email= instance.email)

post_save.connect(get_user_to_public_profile, sender=User)