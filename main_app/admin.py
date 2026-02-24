from django.contrib import admin
from .models import Cat, Feeding, Toy

# Register your models here.
from .models import Cat

admin.site.register(Cat)
admin.site.register(Feeding)
admin.site.register(Toy)
