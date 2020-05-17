from django.urls import path, re_path, include
from .views  import homePage, card_update, checkorders
app_name = 'card'

urlpatterns = [
    path('', homePage, name='home-page'),
    path('update/', card_update, name= 'card-update'),
    path("check/", checkorders, name="check-orders"),
]
