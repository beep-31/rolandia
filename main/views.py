from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def home(request):
    return render(request, template_name='home.html')

@csrf_exempt
def search(request):
    if request.method == 'GET':
        return render(request, template_name='index.html')
    if request.method == 'POST':
        return render(request, template_name='index.html')
