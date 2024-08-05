from django.shortcuts import render

# Create your views here.
def top_page(request):
    return render(request, 'index.html')