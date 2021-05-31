from django.db import models
import bcrypt, re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_val(self,post_data):
        errors = {}
        if len(post_data ['firstname']) < 2:
            # print('The firstname is less than 2 char!')
            errors['firstname'] = 'First name must be at least 2 char!'
        if len(post_data ['lastname']) < 2:
            # print('The lastname is less than 2 char!')
            errors['lastname'] = 'Last name must be at least 2 char!'
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] ='Invalid Email Address'
        if post_data['password'] != post_data['confirm_password']:
            errors['password'] = 'Your password and Confirm Password do not match'
        print('gets inside registration val function')
        emailcheck =self.filter(email=post_data['email'])
        if emailcheck:
            errors['email'] = 'This Email is aleady in use'
        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be greater than 8 char'
       
        return errors
    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())
    
class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    def __str__(self):
        return f"{self.firstname} {self.lastname} {self.email}"
    

class MessageManager(models.Manager):
    def validate_message(self, message_text):
        errors = {}
        if len(message_text)<2:
            errors['length'] = 'You message must be between 2 - 255 character'
        if len(message_text) > 256:
            errors['length'] = 'You message must be between 2 - 255 character'
        return errors

class Message(models.Model):
    user = models.ForeignKey(User, related_name="message", on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = MessageManager()
    
    def __str__(self):
        return f"{self.content}"
    
class Comment(models.Model):
    comment = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    content = models.ForeignKey(Message, related_name='message_comments' , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.content}"