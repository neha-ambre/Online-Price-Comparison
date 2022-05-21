
from django.http import HttpResponse
from django.shortcuts import render
from . import sourceCode

def index(request):
    return render(request, 'index.html')
   
def contact(request):
     return render(request, 'templates/contact.html')

def about(request):
    return HttpResponse("we are at about")

def productView(request):
    records = []
    productName = ""
    if request.method == 'POST':
        productName = request.POST.get('product')
        records = sourceCode.main(productName)
        print(records)
    return render(request, 'productView.html', {'productName':productName,'records':records})
