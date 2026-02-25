from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
#!tangent from Canvas notes
from django.urls import reverse_lazy

from .models import Cat, Toy
from .forms import FeedingForm

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("CONTEXT:", context)
        # toys = Toy.objects.all()
        # toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))
        toys_cat_doesnt_have = Toy.objects.exclude(id__in = self.object.toys.all().values_list('id'))
        context["feeding_form"] = FeedingForm()
        # context['toys'] = toys
        context['toys'] = toys_cat_doesnt_have
        return context

class CatCreate(CreateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']
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

def add_feeding(request, pk):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False) # Save the form but don't commit it yet to the database
        new_feeding.cat_id = pk
        new_feeding.save()

    return redirect("cat-detail", pk=pk)

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyList(ListView):
    model = Toy

class ToyDetail(DetailView):
    model = Toy

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = reverse_lazy('toy-index')

def associate_toy(request, cat_id, toy_id):
    # Note that you can pass a toy's id instead of the whole object
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    # return redirect('cat-detail', cat_id=cat_id)
    return redirect('cat-detail', pk=cat_id)

def remove_toy(request, cat_id, toy_id):
    # Look up the cat
    # Cat.objects.get(id=cat_id).toys.remove(toy_id)
    # Also rewrite above as:
    cat = Cat.objects.get(id=cat_id)
    cat.toys.remove(toy_id)
    # Look up the toy
    # Remove the toy from the cat
    # return redirect('cat-detail', cat_id=cat.id)
    # return redirect('cat-detail', pk=cat.id)
    return redirect('cat-detail', pk=cat_id)





