from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from .views import SeriesBooks, BookList ,BookDeatils
app_name='books'

urlpatterns = [
    re_path(r'^course/list/(?P<slug>[\w-]+)/$', BookList.as_view(), name='book-list'),
    re_path(r'books/(?P<slug>[\w-]+)/$', SeriesBooks.as_view(), name='series-books'),
    re_path(r'course/details/(?P<slug>[\w-]+)/$', BookDeatils.as_view(), name='details-book')
]


