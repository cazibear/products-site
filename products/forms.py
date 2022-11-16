from django import forms
from .models import User

class RegisterForm(forms.Form):
	username = forms.CharField(max_length=20, required=True)
	password = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True)
	name = forms.CharField(max_length=100, required=False)
	email = forms.EmailField(max_length=100, required=True)

	def __init__(self, *args, **kwargs):
		super(RegisterForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
	