from django.shortcuts import render
# from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
#!tangent from Canvas notes
from django.urls import reverse_lazy

from .models import Cat

# Create your views here.
def home(request):
    # Send a simple HTML response
    # return HttpResponse('<h1>Hello ᓚᘏᗢ</h1>')
    return render(request, "home.html")

def about(request):
    # return HttpResponse("<h1>About the CatCollector</h1>")
    return render(request, "about.html")

#! commented out after schema added
# class Cat:
#     def __init__(self, name, breed, description, age):
#         self.name = name
#         self.breed = breed
#         self.description = description
#         self.age = age

#! commented out after schema added
# Create a list of Cat instances
# cats = [
#     Cat('Lolo', 'tabby', 'Kinda rude.', 3),
#     Cat('Sachi', 'tortoiseshell', 'Looks like a turtle.', 0),
#     Cat('Fancy', 'bombay', 'Happy fluff ball.', 4),
#     Cat('Bonk', 'selkirk rex', 'Meows loudly.', 6)
# ]

# def cat_index(request):
#     # Render the cats/index.html template with the cats data
#     cats = Cat.objects.all()  # look familiar?
#     return render(request, 'cats/index.html', {'cats': cats})
#!above replaced by class CatList

class CatList(ListView):
    model = Cat

# def cat_detail(request, cat_id):
#     cat = Cat.objects.get(id=cat_id) # singular
#     return render(request, 'cats/detail.html', {'cat': cat})
#!above replaced by class CatDetail

class CatDetail(DetailView):
    model = Cat

class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
    # success_url = '/cats/'
    #! below is tangent from Canvas notes; commented out after https://pages.git.generalassemb.ly/modular-curriculum-all-courses/django-crud-app-cat-collector/django-class-based-views/#redirecting-to-a-newly-created-cat-object
    # success_url = reverse_lazy('cat-index')

class CatUpdate(UpdateView):
    model = Cat
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    # success_url = '/cats/'
    success_url = reverse_lazy('cat-index')




