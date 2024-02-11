from django.http import HttpResponse
from django.shortcuts import redirect, render
from accounts.models import User, UserProfile
from technician.forms import TechnicianForm
from .forms import UserForm
from django.contrib import messages, auth
from .utils import detectUser 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from technician.models import Technician
# Create your views here.

# Restrict the technician from accessing the customer page
def check_role_technician(user):
  if user.role == 1:
    return True
  else:
    raise PermissionDenied


# Restrict the customer from accessing the technician page
def check_role_customer(user):
  if user.role == 2:
    return True
  else:
    raise PermissionDenied
def registerUser(request):
  if request.user.is_authenticated:
    messages.warning(request, 'You are already logged in!')
    return redirect('myAccount')
  elif request.method == 'POST':  
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
      user = User.objects.create_user(first_name=first_name,last_name=last_name, profile_picture=profile_picture, 
                                      email=email, phone_number=phone_number, username=username, password=password)
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

# def registerTechnician(request):
#   if request.user.is_authenticated:
#     messages.warning(request, 'You are already logged in!')
#     return redirect('myAccount')  
#   elif request.method == 'POST':
#     #store the data and create the user
#     form = UserForm(request.POST)
#     t_form = TechnicianForm(request.POST, request.FILES)
#     if form.is_valid() and t_form.is_valid():
#       first_name = form.cleaned_data["first_name"]
#       last_name = form.cleaned_data["last_name"]
#       username = form.cleaned_data["username"]
#       email = form.cleaned_data["email"]
#       profile_picture = form.cleaned_data['profile_picture']
#       phone_number = form.cleaned_data['phone_number']
#       password = form.cleaned_data["password"]
#       user = User.objects.create_user(first_name=first_name,last_name=last_name, 
#                                       email=email, profile_picture=profile_picture, 
#                                       phone_number=phone_number, username=username, password=password)
#       user.role = User.TECHNICIAN
#       user.save()
#       technician = t_form.save(commit=False)
#       technician.user = user
#       user_profile = UserProfile.objects.get(user=user)
#       technician.user_profile = user_profile
#       technician.save()
#       messages.success(request, "Your account has been registered successfully")
#       return redirect('registerTechnician')  
#     else:
#       print('invalid form')
#       print(form.errors)  
#   else:  
#     form = UserForm()
#     t_form = TechnicianForm()
#   context = {
#     'form': form,
#     't_form': t_form,
#   }
#   return render(request, 'accounts/registerTechnician.html', context)

def registerTechnician(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')  
    elif request.method == 'POST':
        # store the data and create the user
        form = UserForm(request.POST)
        t_form = TechnicianForm(request.POST, request.FILES)
        if form.is_valid() and t_form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            profile_picture = form.cleaned_data['profile_picture']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data["password"]
            
            # Check if 'profile_picture' is in request.FILES
            if 'profile_picture' in request.FILES:
                profile_picture = request.FILES['profile_picture']
            else:
                profile_picture = None

            user = User.objects.create_user(
                first_name=first_name, last_name=last_name, 
                email=email, phone_number=phone_number, 
                username=username, password=password,
                profile_picture=profile_picture  # Passing the profile_picture
            )
            
            user.role = User.TECHNICIAN
            user.save()

            technician = t_form.save(commit=False)
            technician.user = user
            user_profile = UserProfile.objects.get(user=user)
            technician.user_profile = user_profile
            technician.save()

            # Saving the profile picture separately
            if profile_picture:
                user.profile_picture.save(profile_picture.name, profile_picture)

            messages.success(request, "Your account has been registered successfully")
            return redirect('registerTechnician')  
        else:
            print('invalid form')
            print(form.errors)  
    else:  
        form = UserForm()
        t_form = TechnicianForm()
        
    context = {
        'form': form,
        't_form': t_form,
    }
    return render(request, 'accounts/registerTechnician.html', context)



def login(request):
  if request.user.is_authenticated:
    messages.warning(request, 'You are already logged in!')
    return redirect('myAccount')
  elif request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']

    user = auth.authenticate(email=email, password=password)
    
    if user is not None:
      auth.login(request, user)
      messages.success(request, 'You are now logged in.')
      return redirect('myAccount')
    else:
      messages.error(request, 'Invalid Login Credentials')
      return redirect('login')
  return render(request, 'accounts/login.html')

def logout(request):
  auth.logout(request)
  messages.info(request, 'You are logged out.')
  return redirect('login')

@login_required(login_url='login')
def myAccount(request):
  user = request.user
  redirectUrl = detectUser(user)
  return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_technician)
def technicianDashboard(request):
  return render(request, 'accounts/technicianDashboard.html')