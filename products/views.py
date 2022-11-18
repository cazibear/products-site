from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Product
from .forms import RegisterForm, LoginForm


def index(request, message=None):
	""" the index, or homepage of the site """

	context = {
		"recent_products": Product.objects.order_by('-submitted')[:6],
		"user": request.session.get("user"),
		"message": request.GET.get("message")
	} # what variables can be put into the templates
	return render(request, "products/index.html", context)


def register(request):
	""" view for registering a user """

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
			request.session["message"] = f"User {form.cleaned_data['username']} created successfully!"
			return redirect(index)
		else:
			# if form fails, retry the form. this should put any errors in the form
			return render(request, "products/register.html", {"form": form})
	else:
		# if a get or other method just display the form
		form = RegisterForm()
	
	return render(request, "products/register.html", {"form": form})


def login(request):
	""" view to handle logging in or out """

	if request.method == "POST":
		# if a user is trying to login
		form = LoginForm(request.POST) # get the form data
		context = {"form": form}
		if not form.is_valid():
			# if form is invalid let user try again
			render(request, "products/login.html", context)
		else:
			# process the data
			try:
				# get the user that matches the username
				database_user = User.objects.get(username=form.cleaned_data["username"])
				if not check_password(form.cleaned_data["password"], database_user.password):
					# if password doesn't match
					request.session["message"] = "Username and password do not match."
				else:
					# if their password entered into the form matches the database one, log them in
					request.session["user"] = str(database_user)
					# set the session variable "user" to their name then send them back to index
					print("successful login")
					return redirect(index)
			except User.DoesNotExist:
				# exception raised if the username doesn't exist
				request.session["message"] = "No user by this username exists."
			
			# if the login didn't succeed, try again
			context["message"] = request.session.get("message")
			return redirect(login)
	else:
		# create the form and let the user login, or logout
		form = LoginForm()
		context = {"form": form, "user": request.session.get("user")}
		return render(request, "products/login.html", context)


def logout(request):
	""" view for logging the user out """

	del request.session["user"] # remove the login variable, logging them out

	return redirect(index)
	
