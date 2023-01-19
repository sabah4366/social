from rest_framework import  serializers
from django.contrib.auth.models import User
from api.models import Posts,Comments
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    post=serializers.CharField(read_only=True)
    liked_by=serializers.CharField(read_only=True)
    count_commentslikes=serializers.CharField(read_only=True)
    class Meta:
        model=Comments
        fields="__all__"


class PostSerializer(serializers.ModelSerializer):
    image=serializers.CharField(read_only=True)
    date=serializers.CharField(read_only=True)
    id=serializers.CharField(read_only=True)
    likedby=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    post_comments=CommentSerializer(read_only=True,many=True)
    postlike_count=serializers.CharField(read_only=True)

    class Meta:
        model=Posts
        fields="__all__"