from django.db import models
import datetime
import re	# the regex module
import bcrypt

# Add Validation 
class UserManager(models.Manager):
    # Function to check data from form before add it in table
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        # Check first name
        if len(postData['first_name']) < 2:
            errors["first_name"] = []
            errors["first_name"].append("First Name should be at least 2 characters")
        if postData['first_name'].isalpha() == False:
            if "first_name" not in errors:
                errors["first_name"] = []
            errors["first_name"].append("First Name cannot contain numbers or special characters")
        # Check last name
        if len(postData['last_name']) < 2:
            errors["last_name"] = []
            errors["last_name"].append("last Name should be at least 2 characters")
        if postData['last_name'].isalpha() == False:
            if "last_name" not in errors:
                errors["last_name"] = []
            errors["last_name"].append("Last Name cannot contain numbers or special characters")
        # Check email
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):# test whether a field matches the pattern  
            errors["email"] = []
            errors["email"].append("Invalid email address!")
        if is_exists(postData['email']):
            if "email" not in errors:
                errors["email"] = []
            errors["email"].append("The email address you provided is already associated with an existing account. Please choose a different email address or log in if you already have an account.")
        # Check password
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters long"
        # Check confirm password
        if postData['password'] != postData['c_password']:
            errors["c_password"] = "Confirm password should be the same as password"
        # Check birthday 
        current_time = datetime.datetime.today()
        birthday = datetime.datetime.strptime(postData['birthday'],'%Y-%m-%d')
        if birthday > current_time:
            errors["birthday"] = "Birthday cannot be in future"               
        elif birthday.year > current_time.year - 13:
            errors["birthday"] = "Your age should be at least 13 years old"        
        return errors
    

# Create User table in database
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    birthday = models.DateField()
    create_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() 

    # Hash the password before saving
    def save(self, *args, **kwargs):
        if self.password:
            self.password = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt()).decode()
        super().save(*args, **kwargs)

# ******************** C (Create) from CRUD ********************
# This functions is used to add a new show to the Show table 
def register(request_data):
    first_name = request_data['first_name']
    last_name = request_data['last_name']
    email = request_data['email']
    password = request_data['password'] # Hash password
    birthday = request_data['birthday']
    user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=password, birthday=birthday)
    return user

def get_user(email):
    try:
        user = User.objects.get(email=email)
        print("TYPE of user object", type(user))
        return user
    except User.DoesNotExist:
        print("User with email {} does not exist".format(email))
        return None  # Or you can raise an exception if needed

    
# Function to check if the show email is exists or not 
def is_exists(email):
    return User.objects.filter(email=email).exists()

    # def login():
    # # see if the username provided exists in the database
    # user = User.objects.filter(username=request.POST['username']) # why are we using filter here instead of get?
    # if user: # note that we take advantage of truthiness here: an empty list will return false
    #     logged_user = user[0] 
    #     # assuming we only have one user with this username, the user would be first in the list we get back
    #     # of course, we should have some logic to prevent duplicates of usernames when we create users
    #     # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
    #     if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
    #         # if we get True after checking the password, we may put the user id in session
    #         request.session['userid'] = logged_user.id
    #         # never render on a post, always redirect!
    #         return redirect('/success')
    # # if we didn't find anything in the database by searching by username or if the passwords don't match, 
    # # redirect back to a safe route
    # return redirect("/")

# ******************** R (Read one) from CRUD ********************
# This function will reuturn a show information by its ID
# def get_info(id):
#     show = Show.objects.get(id=id)
#     return show

# ******************** R (Read all) from CRUD ********************
# This function is used to return all shows information to display them 
# def get_all_shows():
#     return Show.objects.all()

# ******************** U (Update) from CRUD ********************
# Update show data
# **First we need to get new data from form 
#   Note if the user didn't add anything the value will be the old data
# ** Get show entity 
# ** Update values of entity then save 
# ** Return id to go to shows/show_id
# def update(request_data):
#     id = int(request_data['id'])
#     title = request_data['title']
#     network = request_data['network']
#     release_date = request_data['release_date']
#     description = request_data['description']
#     show = get_info(id)
#     show.title = title
#     show.network = network
#     show.release_date = release_date
#     show.description = description
#     show.save()
#     return id 

# ******************** D (Update) from CRUD ********************
# This function is used to delete specific show by getting its ID
# def delete(id):
#     show = get_info(id)
#     show.delete()
