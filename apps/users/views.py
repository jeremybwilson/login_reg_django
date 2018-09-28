from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import random, datetime, bcrypt

# create a regular expression object that we can use run operations on
# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your views here.
def index(request):
    
    if 'user_id' not in request.session:
        request.session['user_id'] = False
        return redirect('users:index')
    # else:
    #     print "Session 'user_id' status already stored as: " + str(request.session['user_id'])

    if 'logged_in' not in request.session:
        request.session['logged_in'] = False
        return redirect('users:index')
    # else:
    #     print "Session 'logged_in' status already stored as: " + str(request.session['logged_in'])

    todaysDateVariable = datetime.datetime.now().date()
    context = dict(todaysDateVariable = todaysDateVariable)

    return render(request, 'users/index.html', context)

def new(request):
    if 'user_id' not in request.session:
        request.session['user_id'] = False
        print "*" * 80
        print "Session 'user_id' status was not stored, so we set it to: " + str(request.session['user_id'])
        return redirect('users:new')
    
    if 'logged_id' not in request.session:
        request.session['logged_id'] = False
        print "*" * 80
        print "Session 'logged_id' status was not stored, so we set it to: " + str(request.session['logged_id'])
    else:
        return redirect('users:index')

    todaysDateVariable = datetime.datetime.now().date()
    context = dict(todaysDateVariable = todaysDateVariable)

    now = datetime.datetime.now()
    return render(request, 'users/new.html', context)

def create(request):
    if request.method == 'POST':

        valid, result = User.objects.validate_and_create_user(request.POST)

        if valid:
            request.session['user_id'] = result

            # login status & user id => saved to session
            request.session['logged_in'] = True
            request.session['user_id'] = User.objects.get(email=email).id

            # redirect to successful route with message
            messages.success(request, "Successfully, registered and logged in!", extra_tags="registration_success")

            return redirect('users:success')
        else:
            for error in result:
                messages.error(request, error)
            return redirect('users:new')

        if not 'users' in request.session:
            request.session['users'] = [user]
        else:
            request.session['users'].append(user)
            request.session.modified = True
        
        request.session['logged_in'] = True
        return redirect('users:success')
    else:
        errors.append('There was an error with the form.')
        print form_data
        return redirect('users:create')

def show(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except:
        return redirect('/users')

    context = {
        'user' : user,
    }

    return render(request, 'users/show.html', context)

def success(request):
    if 'user_id' not in request.session:
        return redirect('users:index')
    else:
        print "Session 'user_id' status already stored as: " + str(request.session['user_id'])

    if 'logged_in' not in request.session:
        return redirect('users:index')
    else:
        print "Session 'logged_in' status already stored as: " + str(request.session['logged_in'])

    print "*" * 80
    print "This is the 'success' route"
    user_id = int(request.session["user_id"])
    # user = request.session['users'][user_id]
    logged_in_status = request.session['logged_in']
    print "*" * 80

    if request.session['logged_in'] == True:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'first_name': User.objects.get(id=request.session['user_id']).first_name,
            'last_name': User.objects.get(id=request.session['user_id']).last_name,
            'user_id': user_id,
        }
        return render(request, "users/success.html", context)


def login(request):
    if request.method == "POST":

        valid, result = User.objects.login_user(request.POST)
        if not valid:
            for error in result:
                messages.error(request, error)
            return redirect('users:new')
        else:   # Case : successful login 
            request.session['user_id'] = result
            request.session['logged_in'] = valid

            print "*" * 80
            print "This is the 'login' route"
            print "Contents of results variable:", result
            print "Logged ID:", request.session['logged_in']
            # request.session['logged_in'] = True
            # request.session['user_id'] = User.objects.get(email=request.POST["email"]).id

            print "=" * 80
            print "login route user_id is: ", result

            return redirect('users:success')
    else:
        return redirect('users:new')


def logout(request):
  request.session.clear()
  return redirect('users:new')

def delete(request, user_id):

    return redirect('/users')