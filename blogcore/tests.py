from django.test import TestCase
from blogcore.models import Bloguser, Post, Comment
from django.core.urlresolvers import reverse

def create_bloguser(name):
    return Bloguser.objects.create(name = name)

def create_post(title, content, bloguser):
    return Post.objects.create(title = title, content = content, bloguser = bloguser)

def create_comment(content, post, bloguser):
    return Comment.objects.create(content = content, post = post, bloguser = bloguser)

def quick_create_post_with_bloguser():
    bloguser = create_bloguser('Joen')
    post = create_post('Post title', 'This is a post content', bloguser)
    return post

def quick_create_comment():
    bloguser = create_bloguser('Joen')
    comment_user = create_bloguser('Yee')
    post = create_post('Post with comment title', 'This is a content with comment content', bloguser)
    comment = create_comment('This is comment content', post, comment_user)
    return comment

def quick_create_user_with_two_posts_and_four_comments():
    bloguser = create_bloguser('One_Two_Four')
    comment_user1 = create_bloguser('C1')
    comment_user2 = create_bloguser('C2')
    post1 = create_post('Post1', 'Post1 Content', bloguser)
    post2 = create_post('Post2', 'Post2 Content', bloguser)
    create_comment('This is comment1-1 content', post1, comment_user1)
    create_comment('This is comment1-2 content', post1, comment_user2)
    create_comment('This is comment2-1 content', post2, comment_user1)
    create_comment('This is comment2-2 content', post2, comment_user2)
    return bloguser

class IndexViewTests(TestCase):
    
    def test_index_without_content(self):
        contains = ['No blogs!', 'Register', 'About']
        
        response = self.client.get(reverse('blogcore:index'))
        #print(response.content)     #Just want to know what exactly the response is...
        
        self.assertEqual(response.status_code, 200)
        for string in contains:
            self.assertContains(response, string)

    def test_index_with_blogs(self):
        post = quick_create_post_with_bloguser()
        contains = [post.title, post.bloguser.name]
        not_contains = [post.content]
        
        response = self.client.get(reverse('blogcore:index'))
        #print(response.content)
        
        self.assertEqual(response.status_code, 200)
        for string in contains:
            self.assertContains(response, string)
        for string in not_contains:
            self.assertNotContains(response, string)
    
class DetailViewTests(TestCase):
    
    def test_target_not_exists(self):
        response = self.client.get(reverse('blogcore:detail', args = (1, )))
        #print(response.content)
        
        self.assertEqual(response.status_code, 404)
    
    def test_one_target_without_comment(self):
        post = quick_create_post_with_bloguser()
        contains = [post.title, post.content, post.bloguser.name]
        
        response = self.client.get(reverse('blogcore:detail', args = (post.id, )))
        
        self.assertEqual(response.status_code, 200)
        for string in contains:
            self.assertContains(response, string)

    def test_one_target_with_comment(self):
        comment = quick_create_comment()
        post = comment.post
        contains = [post.title, post.content, post.bloguser.name, comment.content, comment.bloguser.name]
        
        response = self.client.get(reverse('blogcore:detail', args = (post.id, )))
        
        self.assertEqual(response.status_code, 200)
        for string in contains:
            self.assertContains(response, string)

class UserListTests(TestCase):
    
    def test_no_user(self):
        contains = ['No blogusers!']

        response = self.client.get(reverse('blogcore:userlist'))
        
        self.assertEqual(response.status_code, 200)
        for string in contains:
            self.assertContains(response, string)
    
    def test_one_user(self):
        user1 = create_bloguser("Judy")
        contains = [user1.name]
        
        response = self.client.get(reverse('blogcore:userlist'))
        
        self.assertEqual(response.status_code, 200)
        for string in contains:
            self.assertContains(response, string)
    
    def test_twenty_users(self):
        users = []
        for i in range(20):
            users.append(create_bloguser("User" + str(i)))
        
        contains = []
        for i in range(10):
            #contains.append(users[i].name)         #Ascending of views. 
            contains.append(users[19 - i].name)     #Descending of views. 
        
        response = self.client.get(reverse('blogcore:userlist'))
        
        self.assertEqual(response.status_code, 200)
        for string in contains:
            self.assertContains(response, string)

class UserDetailViewTests(TestCase):

    def test_user_no_exists(self):
        response = self.client.get(reverse('blogcore:userdetail', args = (1, )))
        
        self.assertEqual(response.status_code, 404)
    
    def user_with_one_post_and_one_comment(self):
        comment = quick_create_comment()
        post = comment.post
        user = post.bloguser        
        contains = [user.name, post.title, post.content, comment.content, comment.bloguser]
        
        response = self.client.get(reverse('blogcore:userdetail', args = (user.id, )))
        
        self.assertEqual(response.status_code, 200)
        for string in contains:
            self.assertContains(response, string)
    
    def user_with_multi_posts_and_multi_comment(self):
        contains = []
        user = quick_create_user_with_two_posts_and_four_comments()
        contains.append(user.name)
        for post in user.post_set.all:
            contains.append(post.title)
            contains.append(post.content)
            for comment in post.comment_set.all:
                contains.append(comment.content)
                contains.apend(comment.bloguser.name)
        
        response = self.client.get(reverse('blogcore:userdetail', args = (user.id, )))
        
        self.assertEqual(response.status_code, 200)
        for string in contains:
            self.assertContains(response, string)
                
        