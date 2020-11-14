from django.contrib import admin
from .models import Poem,Comment,Like,Recommendation,Tag,ExPoet

class poemAdmin(admin.ModelAdmin):
    list_display = ('id','title','owner','content','tag','expoet')
class commentAdmin(admin.ModelAdmin):
    list_display = ('owner','poem_n','content')
class likeAdmin(admin.ModelAdmin):
    list_display = ('owner','poem_n')
class recommendationAdmin(admin.ModelAdmin):
    list_display = ('owner','poem_n')
class tagAdmin(admin.ModelAdmin):
    list_display = ('name',)
class expoetAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Poem,poemAdmin)
admin.site.register(Comment,commentAdmin)
admin.site.register(Like,likeAdmin)
admin.site.register(Recommendation,recommendationAdmin)
admin.site.register(Tag,tagAdmin)
admin.site.register(ExPoet,expoetAdmin)
    
