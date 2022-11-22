from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User, Product
from .forms import RegisterForm, LoginForm, ContactForm


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
					request.session["user_id"] = database_user.id
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
	

def contact(request):
	""" view for the contact form, and handling it """
	context = {"user": request.session.get("user")}

	if request.method == "GET":
		# if the method is a get, just get the form
		form = ContactForm()
	elif request.session.get("user_id") is None:
		# checking if there is a user logged in
		request.session["message"] = "You have to be logged in to contact"
		redirect(index)
	else:
		# for a post with the user logged in
		form = ContactForm(request.POST)
		if form.is_valid():
			# check the form is setup and valid
			subject = form.cleaned_data["subject"]
			message = form.cleaned_data["message"]
			from_email = User.objects.get(id=request.session["user_id"]).email
			# get the users email from their id
			try:
				send_mail(subject, message, from_email, ["contact@example.com"])
				# send out their contact email
			except BadHeaderError:
				return HttpResponse("Invalid header.")
			return redirect(sent) # success, send the user to the success page
	
	context["form"] = form # add the form to the context finally
	return render(request, "products/contact.html", context)



def sent(request):
	""" view for successful contact forms """
	return render(request, "products/contact_sent.html", {"user": request.session.get("user")})
