from django.http import HttpResponse
from django.shortcuts import redirect, render
from accounts.models import User
from .forms import UserForm
from django.contrib import messages

# Create your views here.
def registerUser(request):
  if request.method == 'POST':  
    form = UserForm(request.POST, request.FILES)
    if form.is_valid():
      # Create the user using the form
      # password = form.cleaned_data['password']
      # user = form.save(commit=False)
      # user.set_password(password)
      # user.role = User.CUSTOMER
      # user.save()

      #create user using the create_user method
      first_name = form.cleaned_data["first_name"]
      last_name = form.cleaned_data["last_name"]
      username = form.cleaned_data["username"]
      email = form.cleaned_data["email"]
      profile_picture = form.cleaned_data['profile_picture']
      phone_number = form.cleaned_data['phone_number']
      password = form.cleaned_data["password"]
      user = User.objects.create_user(first_name=first_name,last_name=last_name, profile_picture=profile_picture, email=email, phone_number=phone_number, username=username, password=password)
      user.role = User.CUSTOMER
      user.save()
      messages.success(request, 'Your account has been registered successfully')
      return redirect('registerUser')
    else:
      print('invalid form')
      print(form.errors)
  else:
    form = UserForm()
    
  context = {
    'form': form,
  }
  return render(request, 'accounts/registerUser.html', context)
