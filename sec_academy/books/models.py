import os
import random
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from datetime import datetime
from django.utils.html import mark_safe
from accounts.models import User
# from puplic_profile.models import ProfileUser
# from django.conf import settings

from .utilise.utils_nav import unique_slug_generator_pages
# Create your models here.
# User  = settings.AUTH_USER_MODEL
#####################################Book Categories##################################### 
# create custom def to uplaod images
#  here we will divide the image to name and ext
def change_name(filename):
  basname = os.path.basename(filename)
  name, ext = os.path.splitext(basname)
  return name, ext

# here we save profile image for user in a custome folder
def upload_to(instance, filename):
  new_name = random.randint(1, 123456789)
  name, ext = change_name(filename)
  final_name = f'{new_name}{ext}'
  return f"books/icons/{instance.name}/{final_name}"

class BookCategories(models.Model):
  name      = models.CharField(max_length=150)
  icon      = models.ImageField(upload_to=upload_to)
  slug      = models.SlugField(unique=True, null=True, blank=True)

  def __str__(self):
      return self.name

  def get_absolute_url(self):
      return reverse("books:series-books", kwargs={"slug": self.slug})

  #To appear image in the admin page
  def image_tag(self):
    return mark_safe('<img src="{url}" width="{width}" height="{height}" />'.format(
      url=self.icon.url,
      width=self.icon.width,
      height=self.icon.height
    ))
  
  image_tag.short_description = "Icon"
  

  class Meta:
    verbose_name = 'Books Categories'
    verbose_name_plural = 'Books Categories'

def bookCategories_pre_save_reciver(sender, instance, *args, **kwargs):
  if not instance.slug:
    instance.slug = unique_slug_generator_pages(instance)

pre_save.connect(bookCategories_pre_save_reciver, sender=BookCategories)
  
#####################################Book Series##################################### 
class BookSeries(models.Model):
  book      = models.OneToOneField(BookCategories, on_delete=models.CASCADE)
  name      = models.CharField(max_length=150)
  slug      = models.SlugField(unique=True, null=True, blank=True)
  timestamp = models.DateTimeField(auto_now_add=True)
  update    = models.DateTimeField(auto_now=True)

  def __str__(self):
      return self.name

  def get_absolute_url(self):
      return reverse("books:book-list", kwargs={"slug": self.slug})
  
  class Meta:
    verbose_name = 'Books Series'
    verbose_name_plural= 'Books Series'

def book_series_pre_save_receiver(instance, sender, *args, **kwargs):
  if not instance.slug:
    instance.slug = unique_slug_generator_pages(instance)

pre_save.connect(book_series_pre_save_receiver, sender=BookSeries)

#####################################Book##################################### 
def upload_to_content_book(instance, filename):
  new_name = random.randint(1, 5364789123)
  name, ext   = change_name(filename)
  finalname   = f'{new_name}{ext}'

  return f"books/content/{instance.series.book.name}/{instance.series.name}/{instance.name}/{instance.date.month}-{instance.date.year}/{finalname}"

def upload_cover_book(instance, filename):
  new_name = random.randint(1, 5364789123)
  name, ext   = change_name(filename)
  finalname   = f'{new_name}{ext}'

  return f"books/cover/{instance.series.book.name}/{instance.series.name}/{instance.name}/{instance.date.month}-{instance.date.year}/{finalname}"



class Book(models.Model):
  # I created relationship between book and user to know who will create the book?
  user          = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"staff":True}) 
  series        = models.ForeignKey(BookSeries, related_name='series',on_delete= models.CASCADE)
  name          = models.CharField(max_length=250)
  cover         = models.ImageField(upload_to=upload_cover_book, max_length=300)
  bio           = models.TextField()
  learn         = models.TextField(verbose_name="What you'll learn")
  require       = models.TextField(verbose_name="Requirements")
  description   = models.TextField(verbose_name="Description")
  content       = models.FileField(upload_to=upload_to_content_book, max_length=300)
  price         = models.DecimalField(max_digits=10, decimal_places=2, default= 1000.00)
  slug          = models.SlugField(unique=True, null=True, blank=True)
  date          = models.DateTimeField(default = datetime.now)

  def __str__(self):
      return self.name

  def get_absolute_url(self):
      return reverse("books:details-book", kwargs={"slug": self.slug})  

  def image_tag(self):
    return mark_safe('<img src="{url}" width="{width}" height="{height}" />'.format(
      url = self.cover.url,
      width= 150,
      height=75
    ))

  image_tag.short_description = "Image"
  


  class Meta:
    verbose_name = 'Books'
    verbose_name_plural= 'Books'



def book_pre_save_receiver(instance, sender, *args, **kwargs):
  if not instance.slug:
    instance.slug = unique_slug_generator_pages(instance)

pre_save.connect(book_pre_save_receiver, sender=Book)
  

