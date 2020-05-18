from django.shortcuts import render
from django.views.generic import ListView
from books.models import Book

# Create your views here.

class SearchBooksList(ListView):
  template_name = "search/search_books.html"

  def get_context_data(self, *args, **kwargs):
    context = super(SearchBooksList, self).get_context_data(*args, **kwargs)
    query  = self.request.GET.get("q", None)
    context['query'] = query
    return context
    

  def get_queryset(self, *args, **kwargs):
    query = self.request.GET.get("q", None)
    if query is not None:
      return Book.objects.search(query) 
    return Book.objects.all()
  
    
  
  