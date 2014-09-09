from django.db import models

class Post(models.Model):
    title = models.CharField(max_length = 60)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post)
    content = models.TextField(max_length = 250)
    
    def __str__(self):
        return self.content
        
