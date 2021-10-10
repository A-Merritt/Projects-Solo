from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Message, Comment
import bcrypt


# Create your views here.
def log_and_reg(request):
    if 'userid' in request.session:
        return redirect('/wall')
    return render(request, "log_and_reg.html")

def register(request):
    errors = User.objects.register_validator(request.POST)
    if errors:
        for key, val in errors.items():
            messages.error(request, val)
    else:
        password = request.POST["password"]   
        hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()      
        user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            branch=request.POST['branch'], 
            wars=request.POST['wars'],
            email=request.POST['email'],
            password = hash_pw
        )
        request.session['userid'] = user.id
        messages.success(request, "Successfully registered account.")     
        return redirect('/wall')
    return redirect ('/')

def login(request):
    users = User.objects.filter(email=request.POST['email'])
    if users:
        logged_user = users[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            messages.success(request, "Successfully logged in")
            return redirect('/wall')
        else:
            messages.error(request, "Invalid Email/Password Combo")
    else:
        messages.error(request, "Account not found")
    return redirect ('/')

def index(request):
    context = {
        'user': User.objects.get(id=request.session['userid'])
    }
    return render(request, 'index.html', context)

def logout(request):
    request.session.flush()
    return redirect ('/')

def wall(request):
    context = {
        'user': User.objects.get(id=request.session['userid']),
        'all_messages': Message.objects.all() # we make this line to pass all messages that get posted through this function so it can be brought into our HTML.
    }
    return render(request, 'wall.html', context)

def post_message(request):
    errors = Message.objects.validator(request.POST)
    if errors:
        for key, val in errors.items():
            messages.error(request, val)
    else:       
        Message.objects.create(
            content = request.POST['content'],
            creator = User.objects.get(id=request.session['userid'])
        )
    return redirect('/wall')

def post_comment(request, message_id):
    errors = Comment.objects.validator(request.POST)
    if errors:
        for key, val in errors.items():
            messages.error(request, val)
    else:       
        Comment.objects.create(
            content = request.POST['content'],
            creator = User.objects.get(id=request.session['userid']),
            message = Message.objects.get(id=message_id)  #make sure we pass through the message we want to comment on. 
        )
    return redirect('/wall')

def user(request, user_id):
    context ={
        "user": User.objects.get(id=user_id)
    }
    return render(request, "user.html", context)

def like(request, message_id):
    message = Message.objects.get(id=message_id)
    user = User.objects.get(id=request.session['userid'])
    message.users_who_liked.add(user)
    return redirect('/wall')

def dislike(request, message_id):
    message = Message.objects.get(id=message_id)
    user = User.objects.get(id=request.session['userid'])
    message.users_who_liked.remove(user)
    return redirect('/wall')

def edit(request, message_id):
    context = {
        "message": Message.objects.get(id=message_id),
    }
    return render(request, "edit_message.html", context)

def update(request, message_id):
    errors = Message.objects.validator(request.POST)  # VALIDATOR START - Just copy it from the other validators since it is asking for the same material for input.
    if errors:
        for key, val in errors.items():
            messages.error(request, val)  # VALIDATOR END
            return redirect(f'/messages/{message_id}/edit')  # redirects to edit page since an error was thrown
    else:
        message = Message.objects.get(id=message_id)  #Grab the message you want to update
        message.content = request.POST['content'] #set content to what we entered on edit page
        message.save()  # saves it to the database
    return redirect('/wall')  # redirects to wall since there were no errors and it can be submitted for changes.

def update_user(request, user_id):
    # Make method = 'POST' in HTML
    errors = User.objects.edit_validator(request.POST, user_id)  
    if errors:
        for key, val in errors.items():
            messages.error(request, val)  
            
    else:
        user = User.objects.get(id = user_id) 
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.branch = request.POST['branch']
        user.wars=request.POST['wars']
        user.email = request.POST['email']
        password = request.POST["password"] 
        hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user.password = hash_pw
        user.save()
    return redirect('/index')  

def delete(request, message_id):
    message = Message.objects.get(id=message_id)
    if request.method == 'POST':
        message.delete()
        return redirect('/wall')

def deleteComment (request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('/wall')

def deleteUser (request, user_id):
    user = User.objects.get(id = user_id) 
    if request.method == 'POST':
        user.delete()
        request.session.flush()
        return redirect('/')