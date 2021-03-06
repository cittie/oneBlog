from django.test import TestCase
from django.contrib.auth.models import User
from blogcore.models import UserProfile, Post, Comment, PostForm, CommentForm
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect

def create_user_profile(user):
    return UserProfile.objects.create(user = user)

def create_post(title, content, user_profile):
    return Post.objects.create(title = title, content = content, user_profile = user_profile)

def create_comment(content, post, user_profile):
    return Comment.objects.create(content = content, post = post, user_profile = user_profile)
    
def quick_create_post_with_user():
    user = User.objects.create_user('joen', email = None, password = 'password')
    user_profile = create_user_profile(user)
    post = create_post('Post title', 'This is a post content', user_profile)
    return post

def quick_create_comment():
    user = User.objects.create_user('joen', email = None, password = 'password')
    user_profile = create_user_profile(user)
    comment_user = User.objects.create_user('Yee', email = None, password = 'password')
    comment_user_profile = create_user_profile(comment_user)
    post = create_post('Post with comment title', 'This is a content with comment content', user_profile)
    comment = create_comment('This is comment content', post, comment_user_profile)
    return comment

def quick_create_user_with_two_posts_and_four_comments():
    user = User.objects.create_user('one_two_four', email = None, password = 'password')
    user_profile = create_user_profile(user)
    comment_user1 = User.objects.create_user('C1', email = None, password = 'password')
    comment_user1_profile = create_user_profile(comment_user1)
    comment_user2 = User.objects.create_user('C2', email = None, password = 'password')
    comment_user2_profile = create_user_profile(comment_user2)
    post1 = create_post('Post1', 'Post1 Content', user_profile)
    post2 = create_post('Post2', 'Post2 Content', user_profile)
    create_comment('This is comment1-1 content', post1, comment_user1_profile)
    create_comment('This is comment1-2 content', post1, comment_user2_profile)
    create_comment('This is comment2-1 content', post2, comment_user1_profile)
    create_comment('This is comment2-2 content', post2, comment_user2_profile)
    return user

class RegisterTest(TestCase):
    
    def test_register_normally(self):
        response = self.client.post(reverse('blogcore:register'), {'username': 'user1', 'password1': 'password', 'password2': 'password'})
        #print(response.content)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blogcore:profile_list'))
        
    def test_register_with_incorrect_username(self):
        error_message = "This value may contain only letters, numbers and @/./+/-/_ characters."
        response = self.client.post(reverse('blogcore:register'), {'username': 'XX OO 1982 101 hoho', 'password1': 'password', 'password2': 'password'})
        #print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, error_message)
                
    def test_register_with_incorrect_password(self):
        error_message = "This field is required."
        response = self.client.post(reverse('blogcore:register'), {'username': 'user1', 'password1': '', 'password2': ''})
        #print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, error_message)
                
class LoginTest(TestCase):
    
    def test_user_with_incorrect_username(self):
        response = self.client.post(reverse('blogcore:login'), {'username': 'no_such_name', 'password': 'password'})
        #print(response.content)
        self.assertContains(response, "Sorry, that's not a valid username or password")
        
    def test_user_with_incorrect_passwrod(self):
        response = self.client.post(reverse('blogcore:login'), {'username': 'user1', 'password': 'incorrect_password'})
        #print(response.content)        
        self.assertContains(response, "Sorry, that's not a valid username or password")
            
    def test_user_with_correct_information(self):
        User.objects.create_user("user1", email = None, password = 'password')
        response_post = self.client.post(reverse('blogcore:login'), {'username': 'user1', 'password': 'password'})
        self.assertEqual(response_post.status_code, 302)
        
class LogoutTest(TestCase):
    
    def test_user_logout(self):
        response = self.client.get(reverse('blogcore:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/blogcore/login') 
        #self.assertRedirects(response, '/blogcore/login')    #Django use 302 instead of redirect.    

class IndexViewTests(TestCase):
    
    def test_index_without_content(self):
        contains = ['No blogs!', 'About']       
        response = self.client.get(reverse('blogcore:index'))        
        #print(response.content)     #Just want to know what exactly the response is...
        
        self.assertEqual(response.status_code, 200)
        for string in contains:
            self.assertContains(response, string)

    def test_index_with_blogs(self):
        post = quick_create_post_with_user()
        contains = [post.title, post.user_profile.user.username]
        not_contains = [post.content]
        
        response = self.client.get(reverse('blogcore:index'))
        #print(response.content)
        
        self.assertEqual(response.status_code, 200)
        for string in contains:
            self.assertContains(response, string)
        for string in not_contains:
            self.assertNotContains(response, string)

class PostDetailViewTests(TestCase):
    
    def test_target_not_exists(self):
        response = self.client.get(reverse('blogcore:post_detail', args = (1, )))
        #print(response.content)
        
        self.assertEqual(response.status_code, 404)
    
    def test_one_target_without_comment(self):
        post = quick_create_post_with_user()
        contains = [post.title, post.content, post.user_profile.user.username]

        response = self.client.get(reverse('blogcore:post_detail', args = (post.id, )))
        #print(response.content)
                
        self.assertEqual(response.status_code, 200)
        for string in contains:
            self.assertContains(response, string)

    def test_one_target_with_comment(self):
        comment = quick_create_comment()
        post = comment.post
        contains = [post.title, post.content, post.user_profile.user.username, comment.content, comment.user_profile.user.username]

        response = self.client.get(reverse('blogcore:post_detail', args = (post.id, )))
        #print(response.content)        
        self.assertEqual(response.status_code, 200)
        for string in contains:
            self.assertContains(response, string)

class UserListTests(TestCase):
    
    def test_no_user(self):
        contains = ['No users!']

        response = self.client.get(reverse('blogcore:profile_list'))
        
        self.assertEqual(response.status_code, 200)
        for string in contains:
            self.assertContains(response, string)
    
    def test_one_user(self):
        user1 = User.objects.create_user("judy", email = None, password = 'password')
        create_user_profile(user1)
        contains = [user1.username]
        user1.save()
        
        response = self.client.get(reverse('blogcore:profile_list'))
        
        self.assertEqual(response.status_code, 200)
        for string in contains:
            self.assertContains(response, string)
    
    def test_twenty_users(self):
        users = []
        for i in range(20):
            user = User.objects.create_user("user" + str(i), email = None, password = 'password')
            create_user_profile(user)
            users.append(user)
            user.save()
        
        contains = []
        for i in range(10):
            #contains.append(users[i].username)         #Ascending of views. 
            contains.append(users[19 - i].username)     #Descending of views. 
        
        response = self.client.get(reverse('blogcore:profile_list'))
        #print(response.content)
        
        self.assertEqual(response.status_code, 200)
        for string in contains:
            self.assertContains(response, string)

class UserDetailViewTests(TestCase):

    def test_user_no_exists(self):
        response = self.client.get(reverse('blogcore:profile_detail', args = (1, )))
        
        self.assertEqual(response.status_code, 404)
    
    def test_user_with_one_post_and_one_comment(self):
        comment = quick_create_comment()
        post = comment.post
        user = post.user_profile.user        
        contains = [user.username, post.title, post.content, comment.content, comment.user_profile.user.username]
        
        response = self.client.get(reverse('blogcore:profile_detail', args = (post.user_profile.id, )))
        
        self.assertEqual(response.status_code, 200)
        for string in contains:
            self.assertContains(response, string)
    
    def test_user_with_multi_posts_and_multi_comment(self):
        contains = []
        user = quick_create_user_with_two_posts_and_four_comments()
        user_profile = UserProfile.objects.get(user = user)
        contains.append(user.username)
        
        posts = Post.objects.all().filter(user_profile = user_profile)
        for post in posts:
            contains.append(post.title)
            contains.append(post.content)
            comments = Comment.objects.all().filter(post = post)
            for comment in comments:
                contains.append(comment.content)
                contains.append(comment.user_profile.user.username)
        
        response = self.client.get(reverse('blogcore:profile_detail', args = (user_profile.id, )))
        
        self.assertEqual(response.status_code, 200)
        for string in contains:
            self.assertContains(response, string)

class UserAutheticationTest(TestCase):
    
    def setUp(self):
        self.client.logout()
        #self.client.post(reverse('blogcore:logout'))        
    
    def test_post_create_without_login(self):
        response = self.client.post(reverse('blogcore:post_create'), {'title': 'title', 'content': 'content'})
        #print(response.url)
        self.assertRedirects(response, '/blogcore/login?next=/blogcore/posts/create/', status_code = 302, target_status_code = 301, msg_prefix = '')
        
    def test_post_edit_without_login(self):
        post = quick_create_post_with_user()
        response = self.client.get(reverse('blogcore:post_edit', args = (post.id, )))
        #print(response.url)
        self.assertRedirects(response, '/blogcore/login?next=/blogcore/post/1/edit/', status_code = 302, target_status_code = 301, msg_prefix = '')

class PostCreationTest(TestCase): 
    
    def setUp(self):
        user = User.objects.create_user("username", email = None, password = "password")
        create_user_profile(user)
        login = self.client.login(username = "username", password = "password")
        self.assertTrue(login)       
    
    def test_post_create_correctly(self):
        response = self.client.post(reverse('blogcore:post_create'), {'title': 'title', 'content': 'content'})
        self.assertRedirects(response, '/blogcore/profiles/', status_code = 302, target_status_code = 200, msg_prefix = '')


class PostEditTest(TestCase):
    
    def setUp(self):
        user = User.objects.create_user(username = "username", email = None, password = "password")
        create_user_profile(user)
        login = self.client.login(username = "username", password = "password")
        self.assertTrue(login)
    
    def test_post_edit_correctly(self):
        post = quick_create_post_with_user()
        response = self.client.get(reverse('blogcore:post_edit', args = (post.id, )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)
        self.assertContains(response, post.content)       

