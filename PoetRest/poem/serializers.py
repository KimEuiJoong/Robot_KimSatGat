import os
import sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from rest_framework import serializers
from .models import Poem,Comment,Like,Recommendation,User,PoemTags

#class SurveySerializer(serializers.ModelSerializer):
#    class 
class AdminPoemSerializer(serializers.ModelSerializer):
    expoet = serializers.ReadOnlyField(source='expoet.name')
    tag = serializers.ReadOnlyField(source='tag.name')
    class Meta:
        model = Poem
        fields = ('id','title','content','expoet','tag')

class CommentSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='owner.name')
    class Meta:
        model = Comment
        #fields = '__all__'
        fields = ['id','writer','content']
        #read_only_fields = ('owner','poem_n')

class PoemSerializer(serializers.ModelSerializer):
    #writer = serializers.ReadOnlyField(source='owner.name')
    like = serializers.SerializerMethodField()
    writer = serializers.SerializerMethodField()
    #comments = CommentSerializer(many=True,read_only=True)
    #comments = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    class Meta:
        model = Poem
        #fields = '__all__'
        #fields = ('title','name','content','comments','likenum')
        fields = ('id','title','writer','content','likenum','like')
    def get_like(self,obj):
        if Like.objects.filter(owner=self.context['request'].user,poem_n=obj.id).exists():
            return True
        else:
            return False
    def get_writer(self,obj):
        if obj.owner == User.objects.get(userid="admin"):
            return obj.expoet.name
        else:
            return obj.owner.name
    
class PoemTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoemTags
        fields = () 

class LikeSerializer(serializers.ModelSerializer):
    #writer = serializers.ReadOnlyField(source='owner.name')
    class Meta:
        model = Like
        fields = () 
        #read_only_fields = ('owner','poem_n')

class LikeListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='poem_n.id')
    title = serializers.ReadOnlyField(source='poem_n.title')
    #writer = serializers.ReadOnlyField(source='poem_n.owner.name')
    writer = serializers.SerializerMethodField()
    likenum = serializers.ReadOnlyField(source='poem_n.likenum')
    like = serializers.BooleanField(default=True)
    class Meta:
        model = Like
        #fields = ('poem_id','poem_title','poem_writer','poem_likenum') 
        fields = ('id','title','writer','likenum','like') 
    def get_writer(self,obj):
        if obj.poem_n.owner == User.objects.get(userid="admin"):
            return obj.poem_n.expoet.name
        else:
            return obj.poem_n.owner.name

class LikeNumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poem
        fields = ('likenum',)

class MyPoemListSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='owner.name')
    iflike = False
    like = serializers.SerializerMethodField()
    class Meta:
        model = Poem
        fields = ('id','writer','title','likenum','like')
    def get_like(self,obj):
        if Like.objects.filter(owner=obj.owner,poem_n=obj.id).exists():
            return True
        else:
            return False

class RecommendListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='poem_n.id')
    title = serializers.ReadOnlyField(source='poem_n.title')
    #writer = serializers.ReadOnlyField(source='poem_n.owner.name')
    writer = serializers.SerializerMethodField()
    likenum = serializers.ReadOnlyField(source='poem_n.likenum')
    like = serializers.SerializerMethodField()
    class Meta:
        model = Recommendation
        #fields = ('poem_id','poem_title','poem_writer','poem_likenum') 
        fields = ('id','title','writer','likenum','like') 
    def get_like(self,obj):
        if Like.objects.filter(owner=self.context['request'].user,poem_n=obj.poem_n.id).exists():
            return True
        else:
            return False
    def get_writer(self,obj):
        if obj.poem_n.owner == User.objects.get(userid="admin"):
            return obj.poem_n.expoet.name
        else:
            return obj.poem_n.owner.name
