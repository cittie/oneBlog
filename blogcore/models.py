from django.db import models
from django.core import validators

class Bloguser(models.Model):
    name = models.CharField(max_length = 64,
                            validators = [validators.RegexValidator(regex = '^[a-zA-Z0-9]*$', 
                                                                    message = 'Username must be Alphanumeric', 
                                                                    code = 'invalid_username'),
                                            validators.MinLengthValidator(4),
                                            validators.MaxLengthValidator(14)]
                            )
    created_date = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.name
    
class Post(models.Model):
    bloguser = models.ForeignKey(Bloguser)
    title = models.CharField(max_length = 60)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post)
    bloguser = models.ForeignKey(Bloguser)
    content = models.TextField(max_length = 250)
    created_date = models.DateTimeField(auto_now_add = True)
        
    def __str__(self):
        return self.content


        
