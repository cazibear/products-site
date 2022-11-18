from django import forms
from .models import User

class RegisterForm(forms.Form):
	# form for users to create an account
	username = forms.CharField(max_length=20, required=True)
	password = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True)
	name = forms.CharField(max_length=100, required=False)
	email = forms.EmailField(max_length=100, required=True)

	def __init__(self, *args, **kwargs):
		super(RegisterForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			# giving the fields the bootstrap classes
			visible.field.widget.attrs['class'] = 'form-control'
	
class LoginForm(forms.Form):
	# form for users to login
	username = forms.CharField(max_length=20, required=True)
	password = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True)

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			# giving the fields the bootstrap classes
			visible.field.widget.attrs['class'] = 'form-control'

