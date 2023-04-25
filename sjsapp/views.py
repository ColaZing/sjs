from django.shortcuts import render

# Create your views here.
def cs(request):
    return render(request, 'tasks.html')