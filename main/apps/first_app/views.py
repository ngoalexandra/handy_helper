from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'first_app/index.html')

def process(request):
    # if a form is posted in we will use the validator method which we call -errors-
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        # method is checking if there are any errors
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            # if there are errots this redirects to the user form so they can reenter the correct information
            return redirect(index)
        # if there are no errors, we will continue by hashing the password and entering that information into the DB
        else: 
            hash1= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hash1)
            user.save()
            # information that was posted, we will now put into session
            request.session['id'] = user.id
            request.session['name'] = user.first_name 
            messages.success(request, "Registration was successful")
            return redirect('/')
    

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validation(request.POST)
        #  checks if there are any errors while trying to login in
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            # if there are any errors, redirect to main page
            return redirect('/')
        # otherwise we will get the user info by their email
        email = request.POST['email']
        user = User.objects.get(email = email)
        # whatever id is obtained from the user that is logged in, we will put their id within session
        request.session['id'] = User.objects.get(email = email).id
        # we will also get user's name through the email they logged in with
        request.session['first_name'] = User.objects.get(email = email).first_name
        return redirect('/dashboard')

def dashboard(request):
    if 'id' in request.session:
        context = {
            'users' : User.objects.get(id = request.session['id']),
            # 'this_user_job' : User.objects.filter(id = request.session['id']).uploads,
            'jobs' : Job.objects.all()
        }
        # print(context['this_user_job'])
        return render(request, 'first_app/dashboard.html', context)
    else: 
        return redirect ('/')

def add_process(request):
    if request.method == 'POST':
        errors = Job.objects.job_validation(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/add')
        else:
            Job.objects.create(title = request.POST['title'], desc = request.POST['desc'], location = request.POST['location'], user = User.objects.get(id = int(request.session['id'])))
    return redirect('/dashboard')

def addJob(request):
    return render(request, 'first_app/addjob.html')

def editprocess(request):
    url= "/edit/" + str(request.session['id'])
    if request.method == 'POST':
        if 'id' in request.session:
            errors = User.objects.job_validation(request.POST)
            if len(errors):
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect(url)
        else: 
            job = Job.objects.get( id = request.session['id'])
            job.title = request.POST['title']
            job.desc = request.POST['desc']
            job.location = request.POST['location']
            job.save()
            messages.success(request, "Job was updated")
            return redirect(url)
            
def edit(request, id):
    jobs = Job.objects.get(id = id)
    context = {
        'jobs': jobs
    }
    return render (request, 'first_app/edit.html', context)

def done(request, id):
    delete_job = Job.objects.get(id = id)
    delete_job.delete()
    return redirect('/dashboard')

def view(request, id):
    jobs = Job.objects.filter(id = id)
    context = {
        'jobs': jobs
    }
    return render(request, 'first_app/jobinfo.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def myJob(request):
    user = User.objects.get(id = request.session['id'])
    jobs = Job.objects.filter(user = id)
    context = {
        'jobs': jobs
    }
    return redirect('/dashboard')


