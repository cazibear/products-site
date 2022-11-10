from django.db import models

class Product(models.Model):
	# the model for each product item
	name = models.CharField("The name of the product", max_length=200)
	price = models.DecimalField("The price of the product", max_digits=5, decimal_places=2)
	description = models.TextField("A text description for the item.")
	height = models.DecimalField("The height of the product.", max_digits=5, decimal_places=2)
	width = models.DecimalField("The width of the product.", max_digits=5, decimal_places=2)
	length = models.DecimalField("The length of the product.", max_digits=5, decimal_places=2)

class User(models.Model):
	# the model for each user
	username = models.CharField("What the user uses to login", max_length=20)
	name = models.CharField("What the user chooses to go by", max_length=100)
	password = ""
	email = models.EmailField("The user's email for order confirmations.")
	joined = models.DateField("Date the user joined", auto_now_add=True)
