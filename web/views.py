from django.shortcuts import render
from django.http import HttpResponse
import product.models as products_models

# Index - returns the index page 
def index(request):
    context = {
        "featured" : products_models.Product.getFeaturedProducts(),
    }
    return render(request,"web/index.html",context)