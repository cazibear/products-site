from django.shortcuts import render, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Product
from .forms import RegisterForm

def index(request):
	context = {"recent_products": Product.objects.order_by('-submitted')[:6]}
	return render(request, "products/index.html", context)

def register(request):
	# if a post request, try to register a user
	if request.method == "POST":
		# create a form instance with the post data
		form = RegisterForm(request.POST)
		if form.is_valid():
			# if the form is valid, process the data
			new_user = User(
				username=form.cleaned_data["username"],
				name=form.cleaned_data["name"],
				password=make_password(form.cleaned_data["password"]),
				email=form.cleaned_data["email"]
			)
			# create the new user then save it to the database
			new_user.save()

			# then return the user to the index, showing it was successful
			context = {
				"registered": True,
				"recent_products": Product.objects.order_by('-submitted')[:6]
			}
			return render(request, "products/index.html", context)
		else:
			# if form fails, retry the form. this should put any errors in the form
			return render(request, "products/register.html", {"form": form})
	else:
		# if a get or other method just display the form
		form = RegisterForm()
	
	return render(request, "products/register.html", {"form": form})
