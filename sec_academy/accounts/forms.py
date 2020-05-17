from django import forms
from django.conf import settings
from puplic_profile.models import ProfileUser
from django.http import Http404
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div, Column, Submit
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

User = get_user_model()

class SignUpForm(forms.ModelForm):
  company     = forms.CharField(label='Company', required=False,widget=forms.TextInput(attrs={'placeholder':'Enter name of company (Optional)'}))

  fullname    = forms.CharField(label='Fullname', widget=forms.TextInput(attrs={'placeholder':'Enter Fullname'}))

  iqama       = forms.CharField(label='Iqama', widget=forms.TextInput(attrs={'placeholder':'Enter your number of Iqama'}))

  phone       = PhoneNumberField(region='SA', label='Phone', widget=PhoneNumberPrefixWidget(attrs={'placeholder':'Enter Phone Number'}, initial='SA'))

  

  pass_verf   = forms.CharField(label='verified password',widget=forms.PasswordInput(attrs={'placeholder':'Enter Password again'}))

  class Meta:
    model   = User
    fields  = ('email', 'password',)
    widgets = {
      'email'     : forms.EmailInput(attrs={'placeholder':'Enter your email'}),
      'password'  : forms.PasswordInput(attrs={'placeholder':'Enter Password (at least 8 character)'})
    }

  

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.helper = FormHelper()
    self.helper.layout = Layout(
      Row(
          Column('company', css_class='form-group col-md-6 mb-0'),
          Column('fullname', css_class='form-group col-md-6 mb-0'),
          css_class = 'form-row'
        ),

      Row(
          Column('iqama', css_class='form-group col-md-6 mb-0'),
          Column('phone', css_class='form-group col-md-6 mb-0'),
          css_class = 'form-row'
        ),

      'email',

      Row(
          Column('password', css_class='form-group col-md-6 mb-0'),
          Column('pass_verf', css_class='form-group col-md-6 mb-0'),
          css_class = 'form-row'
        ),

      Submit('submit', 'Sign up')
    )

  '''
    we will create validation for required fields in our form:
    1- Fullname --> we create validation for length letters in fullname #should be at least 8 characters
    2- Iqama --> we create validation for length letter # shold be length letters == 10
    3- Phone --> we create validation for phone is exists or no
    4- Email --> we create validation for uniqe field
    5- Password --> should be strong and at least lenght letter 8
  '''
  # Validation for email if exists or no
  def clean_email(self):
    data = self.cleaned_data
    email = data.get('email')
    qs    = User.objects.filter(email=email)

    if qs.exists():
      raise forms.ValidationError('This email address is already in use.')

    return email

  #Validation for should be strong and at least lenght letter 8
  def clean_password(self, *args, **kwargs):
    password = self.cleaned_data.get('password')
    SpecialSym  = ['$', '@', '#', '%', '!', '^', '&', '*']
    if len(password) < 8:
      raise forms.ValidationError('length should be at least 8')
    if not any(char.isdigit() for char in password):
      raise forms.ValidationError('Password should have at least one numeral')
    if not any(char.isupper() for char in password):
      raise forms.ValidationError('Password should have at least one uppercase letter')
    if not any(char.islower() for char in password):
      raise forms.ValidationError('Password should have at least one lowercase letter')
    if not any(char in SpecialSym for char in password):
      raise forms.ValidationError('Password should have at least one of the symbols $@#')

    return password

  #validation for phone is exists or no
  def clean_phone(self, *args, **kwargs):
    """ validation for phone is exists or no """
    phone = self.cleaned_data.get('phone')
    qs = ProfileUser.objects.filter(phone=phone)
    if qs.exists():
      raise forms.ValidationError('This phone number is already in use.')
    return phone


  def clean_iqama(self, *args, **kwargs):
    """ we create validation for length letter # should be length letters == 10 and it's unique """
    Iqama     = self.cleaned_data.get("iqama")
    qs        = ProfileUser.objects.filter(iqama=Iqama)
    if qs.exists():
      raise forms.ValidationError("This Iqama is already in use.")

    if not Iqama.isdigit():
      raise forms.ValidationError('Iqama should be numbers only')

    if len(Iqama) != 10:
      raise forms.ValidationError('Iqama is wrong should equal 10 numbers')

    return Iqama



  def clean(self, *args, **kwargs):
    data      = self.cleaned_data
    Fullname  = data.get('fullname')
    Password  = data.get('password')
    pass_verf = data.get('pass_verf')
    
    # validation for length letters in fullname
    if len(Fullname) < 8:
      raise forms.ValidationError('Fullname is pretty short should be at least 8 character')
    
    # validation for Password and verified password
    if pass_verf != Password:
      raise forms.ValidationError('Password should be match')
    
    return super().clean(*args, **kwargs)


  def save(self, commit=True):
    user      = super(SignUpForm, self).save(commit=False)
    data      = self.cleaned_data
    user.set_password(self.cleaned_data.get('password'))

    if commit:
      user.save()
    return user


  '''
    We will created function to get the user was created and update his profile
  '''    

  def update_public_profile(self, check=False):
    data      = self.cleaned_data
    company   = data.get('company')
    fullname  = data.get('fullname')
    iqama     = data.get('iqama')
    password  = data.get('password')
    phone     = data.get('phone')
    email     = data.get('email')

    try:
      profile = ProfileUser.objects.filter(email=email)
    except profile.ValueError:
      print("Error in public profile")
    
    
    if check:
      profile.update(company=company, fullname=fullname, iqama=iqama,phone=phone)

    return profile
    
  
###################################### Form Login In ###################################################
'''
  Now we will create a login form via two fields (email, password):
  1- we will use crispy forms
  2- we will create validation for fields
'''
class LoginForm(forms.Form):
  email     = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Enter your Email'}), label='Email')

  password  = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder':'Enter your password'}))

  # play with crispy forms

  def __init__(self, *args, **kwargs):
    super(LoginForm, self).__init__(*args, **kwargs)

    self.helper = FormHelper()
    self.helper.layout = Layout(
      Row(
        Column('email', css_class='form-group col-12 mb-0'),
        Column('password', css_class= 'form-group col-12 mb-0'),
        css_class = 'form-row'
      ),

      Submit('Login', 'submit')
    )

  def clean_email(self, *args, **kwargs):
    email = self.cleaned_data.get('email')
    try:
      User.objects.get(email=email)
    except User.DoesNotExist:
      raise forms.ValidationError('This email not found')

    return email



