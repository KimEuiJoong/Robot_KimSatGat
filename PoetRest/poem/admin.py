from django.contrib import admin
from .models import Poem,Comment,Like,Recommendation,Tag,ExPoet,Feeling,TagScore,Survey,PoemTags

class poemAdmin(admin.ModelAdmin):
    list_display = ('id','title','owner','content','expoet')
    #def tag_name(self, obj):
    #    if obj.tag != None:
    #        return obj.tag.name
    #    else:
    #        return None
    #def expoet_name(self, obj):
    #    if obj.expoet != None:
    #        return obj.expoet.name
    #    else:
    #        return None
class commentAdmin(admin.ModelAdmin):
    list_display = ('owner','poem_n','content')
class likeAdmin(admin.ModelAdmin):
    list_display = ('owner','poem_n')
class recommendationAdmin(admin.ModelAdmin):
    list_display = ('owner','poem_n','date')
    #def tag(self, obj):
    #    if obj.poem_n.tag != None:
    #        return obj.poem_n.tag.name
    #    else:
    #        return None
#class tagAdmin(admin.ModelAdmin):
#    list_display = ('name',)
class expoetAdmin(admin.ModelAdmin):
    list_display = ('name',)
class feelingAdmin(admin.ModelAdmin):
    list_display = ('name',)
class tagAdmin(admin.ModelAdmin):
    list_display = ('name',)
class tagscoreAdmin(admin.ModelAdmin):
    list_display = ('feeling','tag','score')
class surveyAdmin(admin.ModelAdmin):
    list_display = ('owner','feeling','date')
class poemtagsAdmin(admin.ModelAdmin):
    list_display = ('poem','tag')
#    def tag_name(self, obj):
#        return obj.tag.name
#    def feeling_name(self, obj):
#        return obj.feeling.name
admin.site.register(Poem,poemAdmin)
admin.site.register(Comment,commentAdmin)
admin.site.register(Like,likeAdmin)
admin.site.register(Recommendation,recommendationAdmin)
#admin.site.register(Tag,tagAdmin)
admin.site.register(PoemTags,poemtagsAdmin)
admin.site.register(ExPoet,expoetAdmin)
admin.site.register(Feeling,feelingAdmin) 
admin.site.register(Tag,tagAdmin) 
admin.site.register(TagScore,tagscoreAdmin) 
admin.site.register(Survey,surveyAdmin) 
