from django.contrib import admin
from .models import Poem
from .models import Comment

class poemAdmin(admin.ModelAdmin):
    list_display = ('title','owner','content')
class commentAdmin(admin.ModelAdmin):
    list_display = ('owner','poem_n','content')
admin.site.register(Poem,poemAdmin)
admin.site.register(Comment,commentAdmin)
    
