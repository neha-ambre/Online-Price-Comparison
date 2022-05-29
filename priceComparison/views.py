from django.http import HttpResponse
from django.shortcuts import render
from . import sourceCode,microphoneInput
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')
   
def contact(request):
     return render(request, 'contact.html')

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

def convertSpeechToText(request):
    print("Speech to text")
    #if request.method == 'GET':
    speech_text=microphoneInput.speechToText()
    return JsonResponse({'speech_text':speech_text})