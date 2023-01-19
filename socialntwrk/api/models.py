from django.db import models
from django.contrib.auth.models import User

class Posts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=300)
    image=models.ImageField(null=True,upload_to='images')
    date=models.DateTimeField(auto_now_add=True)
    likedby=models.ManyToManyField(User,related_name='likedby')

    def __str__(self):
        return self.title

    @property
    def post_comments(self):
        return self.comments_set.all()

    @property
    def postlike_count(self):
        return self.likedby.all().count()

class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.CharField(max_length=300)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    liked_by=models.ManyToManyField(User,related_name='liked_by')


    def __str__(self):
        return self.comment

    @property
    def count_commentslikes(self):
        return self.liked_by.all().count()
