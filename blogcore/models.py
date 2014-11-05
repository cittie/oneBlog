from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    nickname = models.CharField(max_length = 24)
    gender = models.IntegerField(default = 2)
    avatar = models.IntegerField(default = 0)      # 0 = female, 1 = male, 2 = others
    
    def __str__(self):
        return self.user.username    
 
class Post(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    title = models.CharField(max_length = 60)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post)
    user_profile = models.ForeignKey(UserProfile)
    content = models.TextField(max_length = 250)
    created_date = models.DateTimeField(auto_now_add = True)
        
    def __str__(self):
        return self.content    
