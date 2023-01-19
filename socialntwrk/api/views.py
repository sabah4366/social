from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import  viewsets,serializers
from api.serializers import UserSerializer,PostSerializer,CommentSerializer
from api.models import Posts,Comments
from rest_framework import authentication,permissions
from rest_framework.decorators import action



class UserView(viewsets.ViewSet):
    def create(self,request,*args,**kwargs):
        serialiser = UserSerializer(data=request.data)
        if serialiser.is_valid():
            serialiser.save()
            return Response(data=serialiser.data)
        else:
            return Response(data=serialiser.errors)

class PostView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Posts.objects.all()
    #authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user=request.user
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def list(self, request, *args, **kwargs):
        qs=Posts.objects.all().exclude(user=request.user)
        serializer=PostSerializer(qs,many=True)
        return Response(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        user=request.user
        obj=self.get_object()
        if user==obj.user:
            obj.delete()
            return Response(data='Post deleted')

        else:
            raise serializers.ValidationError('Permission denied for this user')


    def update(self, request, *args, **kwargs):
        user=request.user
        obj=self.get_object()
        if obj.user==user:
            serializer=PostSerializer(data=request.data,instance=obj)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
        else:
            raise serializers.ValidationError('Permission denied for this user')




    @action(methods=["POST"],detail=True)
    def add_comment(self,request,*args,**kwargs):
        obj=self.get_object()
        user=request.user
        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user,post=obj)
            return Response(data=serializer.data)

        else:
            return Response(data=serializer.errors)

    @action(methods=["POST"],detail=True)
    def liked(self,request,*args,**kwargs):
        user=request.user
        obj=self.get_object()
        obj.likedby.add(user)
        return Response(data="post liked")

class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()
    #authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("Method not allowed")

    def list(self, request, *args, **kwargs):
        raise serializers.ValidationError('Method not allowed')

    def destroy(self, request, *args, **kwargs):
        user=request.user
        obj=self.get_object()
        if obj.user==user:
            obj.delete()
            return Response(data="Comment deleted")
        else:
            raise serializers.ValidationError('Permission dennied for this user')

    def update(self, request, *args, **kwargs):
        user=request.user
        obj=self.get_object()
        if obj.user==user:
            serializer=CommentSerializer(data=request.data,instance=obj)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
        else:
            raise serializers.ValidationError('Permission denied for this user')


    @action(methods=["POST"],detail=True)
    def liked(self,request,*args,**kwargs):
        user=request.user
        obj=self.get_object()
        obj.liked_by.add(user)
        return Response(data="Comment liked")
