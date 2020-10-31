from django.contrib import admin
from .models import Poem

class poemAdmin(admin.ModelAdmin):
    list_display = ('title','writer','content')
admin.site.register(Poem,poemAdmin)
    
