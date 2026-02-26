from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
#!tangent from Canvas notes
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
# Add the two imports below
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Import the login_required decorator
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Cat, Toy
from .forms import FeedingForm


# Create your views here.
def home(request):
    # Send a simple HTML response
    # return HttpResponse('<h1>Hello ᓚᘏᗢ</h1>')
    return render(request, "home.html") #? to be commented out


class Home(LoginView):
    template_name = 'home.html'


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
#! above replaced by class CatList


class CatList(LoginRequiredMixin, ListView):
    model = Cat

# filter by user
    def get_queryset(self):
        return Cat.objects.filter(user=self.request.user)

# def cat_detail(request, cat_id):
#     cat = Cat.objects.get(id=cat_id) # singular
#     return render(request, 'cats/detail.html', {'cat': cat})
#! above replaced by class CatDetail


class CatDetail(LoginRequiredMixin, DetailView):
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


class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']
    # success_url = '/cats/'
    #! below is tangent from Canvas notes; commented out after https://pages.git.generalassemb.ly/modular-curriculum-all-courses/django-crud-app-cat-collector/django-class-based-views/#redirecting-to-a-newly-created-cat-object
    # success_url = reverse_lazy('cat-index')
    # This inherited method is called when a valid cat form is being submitted

    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
        # Let the CreateView do its job as usual
        return super().form_valid(form)


class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['breed', 'description', 'age']


class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    # success_url = '/cats/'
    success_url = reverse_lazy('cat-index')


@login_required
def add_feeding(request, pk):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)  # Save the form but don't commit it yet to the database
        new_feeding.cat_id = pk
        new_feeding.save()

    return redirect("cat-detail", pk=pk)


class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'


class ToyList(LoginRequiredMixin, ListView):
    model = Toy


class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy


class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']


class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = reverse_lazy('toy-index')


@login_required
def associate_toy(request, cat_id, toy_id):
    # Note that you can pass a toy's id instead of the whole object
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    # return redirect('cat-detail', cat_id=cat_id)
    return redirect('cat-detail', pk=cat_id)


@login_required
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


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('cat-index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
    # Same as: 
    # return render(
    #     request, 
    #     'signup.html',
    #     {'form': form, 'error_message': error_message}
    # )
