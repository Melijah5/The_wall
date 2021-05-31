from django.shortcuts import render,redirect , HttpResponse
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.registration_val(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val)
            return redirect('/')
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(firstname=firstname, lastname=lastname, email=email, password=hash_pw)
    return redirect('/')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if not User.objects.authenticate(email, password):
            messages.error(request, 'Email and  Password do not match')
            return redirect('/')
        user = User.objects.get(email=email)
        request.session['id']= user.id
        return redirect('/wall')
    # return redirect('/')

def logout(request):
    del request.session['id']
    return redirect('/')

def wall(request):
    if 'id' not in request.session:
        return HttpResponse ("<h1> You must be logged into get the wall page")
    if 'id' in request.session:
        messages = Message.objects.all()
        comments = Comment.objects.all()
        user = User.objects.get(id=request.session['id'])
        context = {
                'messages' : messages,
                'comments' : comments,
                "user": user
            }
        return render(request, 'wall.html', context)
    
   

def add_message(request):
    # content = request.POST['content']
    # errors = Message.objects.validate_message(content)
    # if len(errors) > 0:
    #     for key, val in errors.items():
    #         messages.error(request, val)
    #     return redirect('/wall')
    Message.objects.create(user=User.objects.get(id=request.session['id']), message = request.POST['add_message'])
    messages.success(request, 'You are posted a message successfully!! ')
    return redirect('/wall')



def add_comment(request):
    comment = request.POST['comment']
    message_ID = request.POST['message_ID']
    user = User.objects.get(id=request.session['id'])
    message = Message.objects.get(id=message_ID)
    Comment.objects.create( comment=comment, user=user, content=message)
    return redirect('/wall')

def delete_message(request, message_ID):
    mysite = Message.objects.get(id=message_ID)
    mysite.delete()
    return redirect('/wall')

def edit_message(request, message_ID):
    message_to_edit = Message.objects.get(id=message_ID)
    context = {
        "message" : message_to_edit
    }
    return render(request, 'edit-message.html', context)

def modify_message(request):
    if request.method == 'POST':
        message_ID = request.POST['message_ID']
        new_message = request.POST['mod_message']
        message_to_edit = Message.objects.get(id=message_ID)
        message_to_edit.message = new_message
        message_to_edit.save()
        return redirect('/wall')
        