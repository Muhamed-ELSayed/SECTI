from django.urls import path, re_path, include
from .views import SearchBooksList
app_name = "search"

urlpatterns=[
  path("", SearchBooksList.as_view(), name="search-books")
]