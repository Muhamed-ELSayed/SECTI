from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from .forms import SignUpForm, LoginForm
from .models import ProfileUser
from django.utils.http import is_safe_url


User = get_user_model()
# Create your views here.

'''
  What's we need to in this here:
  1- we need to post data which come from sign up form in your profile 
  2- we need to send email and password to accounts app in user
'''
# def SignupView(request):
#   template_name = 'public_profile/signup.html'
#   form          = SignUpForm(request.POST or None)
#   context       = {'form': form,}
#   next_get = request.GET.get("next")
#   next_post = request.POST.get("next")
#   redirect_path = next_get or next_post or None

#   if request.method == 'POST':
#     form = SignUpForm(request.POST)

#     if form.is_valid():
#       form.save()
#       form.update_user_profile(user=request.user)
#       if is_safe_url(redirect_path, request.get_host()):
#           return redirect(redirect_path)
#       else:
#         return redirect('/')
      
#     else:
#       print('Form invalid', form.errors)

#   else:
#     print('Not Post')
#     form = SignUpForm()


#   return render(request, template_name, context)


# def LoginFormView(request):
#   form = LoginForm(request.POST, None)
#   template_name = 'public_profile/login.html'
#   context = {'form':form}
#   next_get = request.GET.get("next")
#   next_post = request.POST.get("next")
#   redirect_path = next_get or next_post or None

#   if request.method == 'POST':
#     form = LoginForm(request.POST)

#     if form.is_valid():
#       email = form.cleaned_data.get('email')
#       password = form.cleaned_data.get('password')
#       user = authenticate(request, email=email, password=password)
#       if user is not None:
#         login(request,user)
#         if is_safe_url(redirect_path, request.get_host()):
#           return redirect(redirect_path)
#         else:
#           return redirect('/')
#       else:
#         print('Validation login in is invalid')

#     else:
#       print(form.errors)
  
#   else:
#     form = LoginForm()
  
#   return render(request, template_name, context)


# def LogoutForm(request):
#   logout(request)

#   return redirect('/')