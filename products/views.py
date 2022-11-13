from django.shortcuts import render, HttpResponse
from .models import User, Product

def index(request):
	context = {"recent_products": Product.objects.order_by('-submitted')[:6]}
	return render(request, "products/index.html", context)

def users(request):
	user_list = User.objects.all()
	output = ", ".join(str(u) for u in user_list)
	return HttpResponse(output)
