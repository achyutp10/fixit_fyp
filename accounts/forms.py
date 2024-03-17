from django import forms
from .models import User, UserProfile

class UserForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())
  confirm_password = forms.CharField(widget=forms.PasswordInput())
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'profile_picture', 'username', 'email', 'phone_number', 'password',]

  def clean(self):
    cleaned_data = super(UserForm, self).clean()
    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')

    if password != confirm_password:
      raise forms.ValidationError(
        "Password does not match"
      )

class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Start typing...',
        'required': 'required',
        'class': 'form-control', 
    }))
    latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ['address', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude',]
        widgets = {
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'pin_code': forms.TextInput(attrs={'class': 'form-control'}),
        }