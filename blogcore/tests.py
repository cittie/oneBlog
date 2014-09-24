from django.test import TestCase
from blogcore.models import Bloguser, Post, Comment
from django.core.urlresolvers import reverse

def create_bloguser(name):
    return Bloguser.objects.create(name = name)

def create_post(title, content, bloguser):
    return Post.objects.create(title = title, content = content, bloguser = bloguser)

def create_comment(content, post, bloguser):
    return Comment.objects.create(content = content, post = post, bloguser = bloguser)

class IndexViewTests(TestCase):
    
    def test_index_without_content(self):
        response = self.client.get(reverse('blogcore:index'))
        #print(response.content)     #Just want to know what exactly the response is...
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No blog is available!')
        self.assertContains(response, 'Register')
        self.assertContains(response, 'About')

    def test_index_with_blogs(self):
        bloguser = create_bloguser('Joen')
        post = create_post('Hi', 'This is a post', bloguser)
        
        response = self.client.get(reverse('blogcore:index'))
        #print(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)
        self.assertNotContains(response, post.content)
        self.assertContains(response, bloguser.name)