import decimal
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, m2m_changed
from books.models import Book
from datetime import datetime
# Create your models here.
User = settings.AUTH_USER_MODEL
#####################################Card Class##################################### 
class CardQuerySet(models.query.QuerySet):

  '''
    1- we check the card id in session 
    2- we grab the card filter with card id

    conditions
      1- if card id is exists:
          return with card id
          check if the user authenticated and user is none in card to save user in model card
      
      2- if card id is not found:
          we will creating a anonymous user and creating a card id is associated with user id

  '''
  

  def get_card_or_create(self, request):
    card_id = request.session.get('card_id', None)
    qs = self.filter(id=card_id) 
    
    if qs.count() == 1:
      card_obj = qs.first() 
      if request.user.is_authenticated and card_obj.user is None: 
        card_obj.user = request.user
        card_obj.save()
        print('Card ID is exsists')

    else:
      card_obj = self.new(user=None)
      request.session['card_id'] = card_obj.id
      print('The new user id: ', card_obj.id, '\n', 'The new card id: ', card_obj.id)
    return card_obj

  def new(self, user=None):
    user_obj = None
    if user is not None:
      if user.is_authenticated:
        user_obj = user
        print(user)
    return self.model.objects.create(user=user)


class CardManager(models.Manager):
  def get_queryset(self):
    return CardQuerySet(self.model, using= self._db)

  def new(self, user=None):
    return self.get_queryset().new(user=user)

  def get_card_or_create(self,request):
    return self.get_queryset().get_card_or_create(request)

class CardModel(models.Model):
  user      = models.ForeignKey(User, on_delete= models.CASCADE, blank= True, null= True)
  books     = models.ManyToManyField(Book, blank=True, related_name='card')
  subtotal  = models.DecimalField(max_digits= 10, decimal_places=2, default='0.00')
  total     = models.DecimalField(max_digits= 10, decimal_places=2, default='0.00')
  seat      = models.PositiveIntegerField(default=0)
  date      = models.DateTimeField(default=datetime.now)
  objects   = CardManager()

  def __str__(self):
    
    return str(self.id)

  class Meta:
    verbose_name = 'Card'
    verbose_name_plural= 'Cards'

'''
  Create a signal between a card and books to calculate the price of courses
  How to do that:
  1- we will create a functioning receiver with card model
  2- we will create a m2m_changed because of the relationship between card and books is many to many
'''

def card_signal_books(instance, action, sender, *args, **kwargs):  
  books = instance.books.all()
  
  total_books     = 0
  subtotal        = 0
  seats_num       = 0
  for book in books:
    subtotal      += book.price
    vat           = decimal.Decimal(0.05)
    total_books   = subtotal + (subtotal * vat)
  
  instance.total = total_books
  instance.subtotal = subtotal
  instance.save()


m2m_changed.connect(card_signal_books, sender=CardModel.books.through)





  
