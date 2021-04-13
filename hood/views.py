from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import neighbourhood,healthservices,Business,Health,Authorities,BlogPost,Profile,notifications,Comment
# from .email import send_priority_email
from .forms import notificationsForm,ProfileForm,BlogPostForm,BusinessForm,CommentForm
from decouple import config,Csv
import datetime as dt
from django.http import JsonResponse
import json
from django.db.models import Q
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie

# from chartsey.authentication.forms import RegistrationForm
from django.template import RequestContext
from rest_framework.response import Response
from rest_framework.views import APIView
# from .serializer import


# Create your views here.
@ensure_csrf_cookie
def index(request):
    try:
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')
        current_user=request.user
        profile =Profile.objects.all()
    except ObjectDoesNotExist:
        return redirect('create-profile')

    return render(request,'pages/index.html')

@login_required(login_url='/accounts/login/')
def notification(request):
    current_user=request.user
    profile=Profile.objects.all()
    all_notifications = notifications.objects.filter()

    return render(request,'pages/notifications_form.html',{"notifications":all_notifications})

    # return render(request,'pages/notifications.html')



@login_required(login_url='/accounts/login/')
def blog(request):
    current_user=request.user
    profile=Profile.objects.all()
    blogposts = BlogPost.objects.filter()

    # return render(request,'pages/blog.html')

    return render(request,'pages/blog.html',{"blogposts":blogposts})

@login_required(login_url='/accounts/login/')
def health(request):
    current_user=request.user
    profile=Profile.objects.all()
    healthservices = Health.objects.filter()

    # return render(request,'pages/health.html')

    return render(request,'pages/health.html',{"healthservices":healthservices})

@login_required(login_url='/accounts/login/')
def authorities(request):
    current_user=request.user
    profile=Profile.objects.all()
    authorities = Authorities.objects.filter()
    # return render(request,'pages/authorities.html')

    return render(request,'pages/authorities.html',{"authorities":authorities})

@login_required(login_url='/accounts/login/')
def businesses(request):
    current_user=request.user
    profile=Profile.objects.all()
    businesses = Business.objects.filter()
    # return render(request,'pages/businesses.html')

    return render(request,'pages/businesses.html',{"businesses":businesses})

@login_required(login_url='/accounts/login/')
def view_blog(request,id):
    current_user = request.user

    try:
        comments = Comment.objects.filter(post_id=id)
    except:
        comments =[]

    blog = BlogPost.objects.get(id=id)
    if request.method =='POST':
        form = CommentForm(request.POST,request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.username = current_user
            comment.post = blog
            comment.save()
    else:
        form = CommentForm()

    # return render(request,'pages/view_blog.html')

    return render(request,'pages/view_blog.html',{"blog":blog,"form":form,"comments":comments})

@login_required(login_url='/accounts/login/')
def my_profile(request):
    current_user=request.user
    profile=Profile.objects.all()
    # return render(request,'pages/user_profile.html')

    return render(request,'pages/user_profile.html',{"profile":profile})


@login_required(login_url='/accounts/login/')
def user_profile(request,username):
    user = User.objects.all(username=username)
    profile =Profile.objects.all()
    
    # return render(request,'pages/user_profile.html')

    return render(request,'pages/user_profile.html',{"profile":profile})

@login_required(login_url='/accounts/login/')
def new_blogpost(request):
    current_user=request.user
    profile =Profile.objects.all()

    if request.method=="POST":
        form =BlogPostForm(request.POST,request.FILES)
        if form.is_valid():
            blogpost = form.save(commit = False)
            blogpost.username = current_user
            blogpost.neighbourhood = profile.neighbourhood
            blogpost.avatar = profile.avatar
            blogpost.save()

        return HttpResponseRedirect('/blog')

    else:
        form = BlogPostForm()

    # return render(request,'pages/blogpost_form.html')

    return render(request,'pages/blogpost_form.html',{"form":form})

@login_required(login_url='/accounts/login/')
def new_business(request):
    current_user=request.user
    profile =Profile.objects.all()

    if request.method=="POST":
        form =BusinessForm(request.POST,request.FILES)
        if form.is_valid():
            business = form.save(commit = False)
            business.owner = current_user
            business.neighbourhood = profile.neighbourhood
            business.save()

        return HttpResponseRedirect('/businesses')

    else:
        form = BusinessForm()

    # return render(request,'pages/businesses_form.html')

    return render(request,'pages/business_form.html',{"form":form})


@login_required(login_url='/accounts/login/')
def create_profile(request):
    current_user=request.user
    if request.method=="POST":
        form =ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.username = current_user
            profile.save()
        return HttpResponseRedirect('/')

    else:

        form = ProfileForm()
    # return render(request,'pages/profile_form.html')

    return render(request,'pages/profile_form.html',{"form":form})

@login_required(login_url='/accounts/login/')
def new_notification(request):
    current_user=request.user
    profile =Profile.objects.all()

    if request.method=="POST":
        form =notificationsForm(request.POST,request.FILES)
        if form.is_valid():
            notification = form.save(commit = False)
            notification.author = current_user
            notification.neighbourhood = profile.neighbourhood
            notification.save()

            # if notification.priority == 'High Priority':
            #     send_priority_email(profile.name,profile.email,notification.title,notification.notification,notification.author,notification.neighbourhood)

        return HttpResponseRedirect('/notifications')


    else:
        form = notificationsForm()

    # return render(request,'pages/new/notification_form.html')

    return render(request,'pages/notifications_form.html',{"form":form})

@login_required(login_url='/accounts/login/')
def update_profile(request):
    current_user=request.user
    if request.method=="POST":
        instance = Profile.objects.all()
        
        form =ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.username = current_user
            profile.save()

        return HttpResponseRedirect('/update')

    elif Profile.objects.all():
        profile = Profile.objects.all()
        form = ProfileForm()
    else:
        form = ProfileForm()

        return render(request,'pages/update-profile.html',{"form":form})

        # return render(request,'pages/update_profile.html')



@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'blog' in request.GET and request.GET["blog"]:
        search_term = request.GET.get("blog")
        searched_blogposts = BlogPost.search_blogpost(search_term)
        message=f"{search_term}"

        print(searched_blogposts)

        return render(request,'pages/search.html',{"message":message,"blogs":searched_blogposts})

    else:
        message="You haven't searched for any term"
        return render(request,'pages/search.html',{"message":message})
