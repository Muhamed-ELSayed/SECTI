from django.contrib import admin
from .models import BookCategories, BookSeries, Book

# Register your models here.
class BookCategoryAdmin(admin.ModelAdmin):
  fields = ["name","slug","icon",'image_tag']
  readonly_fields = ['image_tag']
  list_display = ["__str__", "slug", 'image_tag']


class BookAdmin(admin.ModelAdmin):
  fieldsets = [("Who's created this book? | Whats series of the book?",{"fields":("user", "series")}),
               ("Upload the cover and the intro video",{"fields":("name", "cover", "image_tag", "content")}),
               ("Basic Information",{"fields":("bio", "learn", "require", "description")}),
               ("Price and Date",{"fields":("price", "date", )}),
              ]
  list_display=["user", "series", "slug", "image_tag"]
  readonly_fields = ["slug", "image_tag"]

# custom amdin for book model
admin.site.register(BookCategories, BookCategoryAdmin)
admin.site.register(BookSeries)
admin.site.register(Book,BookAdmin)
