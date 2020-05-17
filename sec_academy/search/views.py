from django.shortcuts import render
from django.views.generic import ListView
from books.models import Book

# Create your views here.

class SearchBooksList(ListView):
  template_name = "books/seriese_books.html"

  def get_queryset(self, *args, **kwargs):
    query = self.request.GET.get("q")
    if query is not None:
      return Book.objects.filter(name__icontains=query)
    return Book.objects.none()
    
  
    
  
  