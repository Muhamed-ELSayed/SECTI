import re
from django import template
from ..models import BookCategories, BookSeries, Book

register = template.Library()
template_name_categories = 'books/categories.html'
template_name_series = 'books/series_books.html'
template_name_book = 'books/list_book.html'

# create a custome tag for categories books
@register.inclusion_tag(template_name_categories, takes_context=True)
def categories(context):
  qs = BookCategories.objects.all()
  return {'context':context}

# create a custome tag for series books
@register.inclusion_tag(template_name_series, takes_context=True)
def seriesbooks(context):
  context = BookSeries.objects.all()
  return {'context':context}


# create a custome tag for books
@register.inclusion_tag(template_name_book, takes_context=True)
def book(context, *args, **kwargs):
  # print('this is path', context['request'].path)
  # if context['request'].path == '/':
  #   context = Book.objects.filter(series__name='Web Development')
  # else:
  context = Book.objects.all()
  return {"context": context,}
