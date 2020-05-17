from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

# Display home page
def HomePage(request):
  template_name = 'core/home.html'
  return render(request, template_name, {})