from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book, Location
from card.models import CardModel
# Create your views here.

# create a list class for series book
class SeriesBooks(ListView):
  template_name = 'books/seriese_books.html'
  def get_context_data(self, *args, **kwargs):
    print(self.request.GET.get("q"))
    context = super(SeriesBooks, self).get_context_data(*args, **kwargs)
    return context

class BookList(ListView):
  def get_queryset(self, *args, **kwargs):
    slug = self.kwargs.get('slug')
    instance = Book.objects.filter(series__slug=slug)
    return instance

class BookDeatils(DetailView):
  '''
    What we do here:
    1- we grab a spacific course via slug which comes form listview
    2- we create a session for book if not found. 
    3- we send a spacefic course for card page
  '''
  template_name = 'books/book_detail.html'

  def get_context_data(self, *args,**kwargs):
    context = super(BookDeatils, self).get_context_data(*args, **kwargs)
    context['card'] = CardModel.objects.get_card_or_create(self.request)
    book_name = context["object"]
    context["loc"] = Location.objects.filter(book__name=book_name)
    context["bookSeats"] = 0

    # Sum seats in all location
    for obj in context["loc"]:
      context["bookSeats"] += obj.seats
    
    return context
        
  def get_object(self, *args, **kwargs):
    slug = self.kwargs.get("slug")
    instance = Book.objects.get(slug= slug)
    return instance
    
