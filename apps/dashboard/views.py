from django.shortcuts import render, HttpResponse, redirect
import random
# Create your views here.

def index(request):
    print '*' * 80
    print request.session['logged_in']
    return render(request, 'dashboard/index.html')

def process(request):
    if request.method == "POST":
      return redirect('/dashboard/show')
    else:
        return redirect('/dashboard')

def show(request):

    return render(request, 'dashboard/show.html')

def reset(request):
  request.session.clear()
  return redirect('/')