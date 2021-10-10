from django.db import models
from django import forms
import re

# Create your models here.

class MessageManager(models.Manager):  #Since we create a model Message, we need a validator for this model so we can make sure we get valid input from the web user.
    def validator(self, postData):
        errors = {}
        if len(postData['content']) < 1:
            errors['content'] = "Message cannot be blank."
        return errors

class CommentManager(models.Manager):  #Since we create a model Message, we need a validator for this model so we can make sure we get valid input from the web user.
    def validator(self, postData):
        errors = {}
        if len(postData['content']) < 1:
            errors['content'] = "Comment cannot be blank."
        return errors

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        users = User.objects.filter(email=postData["email"])
        if users:
            errors['existing_user'] = "Account with email already exists"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):               
            errors['email'] = ("Invalid email address!")
        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First Name should be at least 2 Characters."
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 Characters."
        # if postData["branch"] == postData["-- Please Select Your Branch Below --"]:
        #     errors["branch"] = "Please Select a Branch of Service."
        if len(postData["password"]) < 8:
            errors["password"] = "Password should be at least 8 Characters."
        if postData["password"] != postData["confirm_password"]:
            errors["confirm_password"] = "Passwords must match"
        return errors

    def login_validator(self, postData):
        errors = {}
        users = User.objects.filter(email=postData["email"])
        if len(postData['email']) < 1:
            errors['email'] = "Email cannot be blank."
        if len(postData["password"]) < 8:
            errors["password"] = "Password should be at least 8 Characters."
        return errors
    
    def edit_validator(self, postData, user_id):
        errors ={}
        users = User.objects.filter(email=postData["email"])
        user_tied_to_email = users[0] 
        if users:
            my_user = User.objects.get(id=user_id)
            if my_user.email != user_tied_to_email.email:
                errors["email"] = "Email is already in use"
            if len(postData["first_name"]) < 2:
                errors["first_name"] = "First name requires at least 2 characters"
            if len(postData["last_name"]) < 2:
                errors["last_name"] = "Last name requires at least 2 characters"
            if len(postData["password"]) < 8:
                errors["password"] = "Password requires at least 8 characters"
            if postData["password"] != postData["confirm_password"]:
                errors["confirm_password"] = "Passwords must match"
        return errors


BRANCH_CHOICES = (
    ('Army', 'ARMY'),
    ('Navy', 'NAVY'),
    ("Marines", "MARINES"),
    ("Air Force", "AIR FORCE"),
    ("Coast Guard", "COAST GUARD"),
    ("Space Force", "SPACE FORCE"),
)

class User(models.Model):
    photo = models.ImageField(blank=True, null=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    branch = models.CharField(max_length=30)
    wars = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null=True)
    objects = UserManager()

class Message(models.Model):
    content = models.TextField()
    creator = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    users_who_liked = models.ManyToManyField(User, related_name="messages_user_liked")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

class Comment(models.Model):
    content = models.TextField()
    creator = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name="comments", on_delete=models.CASCADE, null=True)
    users_who_liked = models.ManyToManyField(User, related_name="comments_user_liked")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()