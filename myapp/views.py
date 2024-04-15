from django.shortcuts import render, redirect
from . import models
import bcrypt

# Root route render a page where users can register or log in
def index(request):
    return render(request,"index.html")

# Function to handle Registration
def register(request):
    if request.method == 'POST':
        errors = models.User.objects.basic_validator(request.POST)
        if len(errors) > 0:
        # If the errors dictionary contains anything redirect the user back to the form to fix the errors
            context = {'errors':errors}
            return render(request,'index.html',context)
        else:
            # If the errors object is empty, that means there is no errors!
            user = models.register(request.POST)
            request.session['login'] = True
            request.session['user_id'] = user.id 
            request.session['email'] = user.email
            return redirect("/success")

def open_home(request):
    if request.session['login'] == True:
        # If the user just register then go to home page
        if 'user_id' in request.session:
            context = {'user':models.get_user(request.session['email'])}
            return render(request,"home.html",context)
        # If the user logged in then go to home page

    else: 
        # Else render a template containing the SweetAlert message and go back to root route
        return render(request, "not_logged_in.html")

# Log out 
def logout(request):
    request.session.clear()
    request.session['login'] = False
    return redirect('/')

# Log in 
def login(request):
    errors = {}
    if request.method == 'POST':
        # Check the email address
        if (models.is_exists(request.POST['email'])):
            # If the email in DB, then check the password
            user = models.get_user(request.POST['email'])
            # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                # if we get True after checking the password, we may put the user id in session
                request.session['user_id'] = user.id
                request.session['login'] = True
                request.session['email'] = user.email
                return redirect('/success')
            else: 
                errors['login_password'] = 'Incorrect password please try again'
                context = {'errors':errors}
                return render(request,'index.html',context)
        # Email is not in database
        else:
            errors['login_email'] = 'Invalid Email address'
            context = {'errors':errors}
            return render(request,'index.html',context)       