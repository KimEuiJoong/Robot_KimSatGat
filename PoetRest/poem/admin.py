from django.contrib import admin
from .models import Poem,Comment,Like,Recommendation

class poemAdmin(admin.ModelAdmin):
    list_display = ('title','owner','content')
class commentAdmin(admin.ModelAdmin):
    list_display = ('owner','poem_n','content')
class likeAdmin(admin.ModelAdmin):
    list_display = ('owner','poem_n')
class recommendationAdmin(admin.ModelAdmin):
    list_display = ('owner','poem_n')
admin.site.register(Poem,poemAdmin)
admin.site.register(Comment,commentAdmin)
admin.site.register(Like,likeAdmin)
admin.site.register(Recommendation,recommendationAdmin)
    
