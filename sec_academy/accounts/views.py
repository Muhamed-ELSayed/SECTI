from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils.http import is_safe_url
from .forms import SignUpForm, LoginForm
# Create your views here.


# we will create register form
def SignupView(request):
  """ 
    we will get form data and create user in accounts app, automatic public profile for this user it be  created so we need to save email and password in user app and another data will save in public profile
  """

  form          = SignUpForm(request.POST or None)
  template_name = "accounts/signup.html"
  success_url   = "/"
  context       = {'form': form,}
  next_get = request.GET.get("next")
  next_post = request.POST.get("next")
  redirect_path = next_get or next_post or None

  if request.method == "POST":
    form = SignUpForm(request.POST)

    if form.is_valid():
      form.save()
      form.update_public_profile(check=True)

      if is_safe_url(redirect_path, request.get_host()):
          return redirect(redirect_path)
      else:
        return redirect('/')

    else:
      print('Form invalid', form.errors)

  return render(request, template_name, {"form":form})


def LoginFormView(request):
  form = LoginForm(request.POST, None)
  template_name = 'accounts/login.html'
  context = {'form':form}
  next_get = request.GET.get("next")
  next_post = request.POST.get("next")
  redirect_path = next_get or next_post or None

  if request.method == 'POST':
    form = LoginForm(request.POST)

    if form.is_valid():
      email = form.cleaned_data.get('email')
      password = form.cleaned_data.get('password')
      user = authenticate(request, email=email, password=password)
      if user is not None:
        login(request,user)
        if is_safe_url(redirect_path, request.get_host()):
          return redirect(redirect_path)
        else:
          return redirect('/')
      else:
        print('Validation login in is invalid')

    else:
      print(form.errors)
  
  else:
    form = LoginForm()
  
  return render(request, template_name, context)


