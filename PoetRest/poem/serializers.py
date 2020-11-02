from rest_framework import serializers
from .models import Poem,Comment,Like


class CommentSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='owner.name')
    class Meta:
        model = Comment
        #fields = '__all__'
        fields = ['id','writer','content']
        #read_only_fields = ('owner','poem_n')

class PoemSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='owner.name')
    #comments = CommentSerializer(many=True,read_only=True)
    #comments = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    class Meta:
        model = Poem
        #fields = '__all__'
        #fields = ('title','name','content','comments','likenum')
        fields = ('id','title','writer','content','likenum')


class LikeSerializer(serializers.ModelSerializer):
    #writer = serializers.ReadOnlyField(source='owner.name')
    class Meta:
        model = Like
        fields = () 
        #read_only_fields = ('owner','poem_n')

class LikeListSerializer(serializers.ModelSerializer):
    poem_id = serializers.ReadOnlyField(source='poem_n.id')
    poem_title = serializers.ReadOnlyField(source='poem_n.title')
    poem_writer = serializers.ReadOnlyField(source='poem_n.writer')
    poem_likenum = serializers.ReadOnlyField(source='poem_n.likenum')
    class Meta:
        model = Like
        fields = ('poem_id','poem_title','poem_writer','poem_likenum') 

class MyPoemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poem
        fields = ('id','title','likenum')
