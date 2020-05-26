from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import CardModel
from books.models import Book
from orders.models import OrdersModel
# Create your views here.
def create_user(user=None):
  return CardModel.objects.create(user=user)
  
def homePage(request):
  card_obj = CardModel.objects.get_card_or_create(request)
  return render(request, 'card/home.html', {'card':card_obj})

def card_update(request):
  '''
    What we do here:
    1- we need to grab book via request id
    2- we add the book in card session
    3- we redirect to card home
  '''
  book_id = request.POST.get('book_id')
  if book_id is not None:
    book_obj = Book.objects.get(id=book_id)
    card_obj = CardModel.objects.get_card_or_create(request)

    if book_obj in card_obj.books.all():
      card_obj.books.remove(book_obj)
      added = False
    else:
      added = True
      card_obj.books.add(book_obj)
    card_count = card_obj.books.count()
    request.session['card_item'] = card_count

  else:
    print('The Book Id Not Found')
    return redirect('card:home-page')
  
  if request.is_ajax():
    data={
      "add": added,
      "remove": not added,
      "cardCount": card_count
    }
    return JsonResponse(data)
    
    
  return redirect('card:home-page')


def checkorders(request):
  template_name = "card/checkout_orders.html"
  card_obj = CardModel.objects.get_card_or_create(request)
  order_obj, new_order_obj = OrdersModel.objects.get_or_create(card=card_obj)

  print(new_order_obj)
  context={"object":order_obj}
  return render(request, template_name, context)