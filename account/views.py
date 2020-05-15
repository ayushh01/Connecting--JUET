from django.shortcuts import render , redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Createpost ,Friend
from django.db.models import Q

def change_friends(request,operation, pk):
	friend = User.objects.get(pk=pk)
	if operation == 'add':
		Friend.add_request(request.user, friend)
	elif operation == 'cancel':
		Friend.cancel_request(request.user, friend)
	elif operation == "accept":
		Friend.accept_request(request.user, friend)
	elif operation == "reject":
		Friend.reject_request(request.user, friend)
	elif operation == 'remove':
		Friend.lose_friend(request.user, friend)
	return redirect('findfriend')

def info(request):
	return render(request , 'account/info.html')

def commentpost(request , pk):
	print(request.POST)
	comm, notif = Comments.objects.get_or_create(user=Profile.objects.get(user=request.user) ,commentData=request.POST.get("comment_d"))
	if(notif):
		comm.save()

	Createpost.objects.get(id=pk).comments.add(comm)
	return HttpResponseRedirect('/conjuet/login/profile')

def showcomment(request , pk):
	comts = Comments.objects.all().order_by('-postedOn')
	post = Createpost.objects.get(pk=pk)
	content = { 'post':post ,'comts':comts }
	return render(request , 'account/showcomment.html' , content)



def deletepost(request , pk):
	newpost = Createpost.objects.get(pk=pk).delete()
	return HttpResponseRedirect('/conjuet/login/profile')


def profilehome(request , pk=None):
	if pk:
		user = User.objects.get(pk=pk)
		
	else:
		user = request.user
		if request.method == "POST":
			uploaded_file = request.FILES['document']			
			print(uploaded_file.name)
			print(uploaded_file.size)
			Pro = Profile.objects.get(user=user).delete()
			data1 , notif = Profile.objects.get_or_create(user=user,image=uploaded_file)
			if(notif):
				data1.save()


		
		
	args = {'user':user }		
	return render(request , 'account/profilehome.html' , args)


# Create your views here.
def register(request):
	if request.method=="POST":
		params=request.POST
		print("no")
		user, notif=User.objects.get_or_create(username=params['enrollno'])
		if(notif):
			user.set_password(params['password'])
			user.email=params['email']
			user.save()
			data1, notif= data.objects.get_or_create(name=user, dob=params['dob'])
			if(notif):
				data1.save()
				return HttpResponseRedirect('/conjuet/login')
			else:
				return HttpResponse("error")
		else:
			return HttpResponse("<h1>Account  Already Created</h1>")
	else:
		return render(request , 'account/register.html')


def notification(request):
	notifications = Notifications.objects.filter(fromUser=request.user).order_by('-created')
	requests = FriendFormation.objects.filter(fromUser=request.user)
	context = { 'notifications':notifications , 'friends':requests}
	return render(request , 'account/notification.html' , context)


def findfriend(request):
	requests = FriendFormation.objects.filter(Q(fromUser=request.user) | Q(toUser=request.user))
	users = User.objects.exclude(id=request.user.id).exclude(Q(id__in = FriendFormation.objects.filter(fromUser=request.user).values('toUser__id')) | Q(id__in = FriendFormation.objects.filter(toUser=request.user).values('fromUser__id')))
	print(users)
	print(requests)
	print(FriendFormation.objects.filter(fromUser=request.user).values('fromUser__id'))
	
	context = { 'users': users , 'friends':requests}
	return render(request , 'account/findfriend.html', context)


@login_required
def profile(request):
	if(request.method=="POST"):
		print("Error1")
		if request.POST.get('content'):
			post=Createpost()
			post.user=request.user
			post.content=request.POST.get('content')
			post.save()
			print("done")
			user = User.objects.filter(username='171b0411')
			newpost = Createpost.objects.all().order_by('-date_posted')
			data1 = data.objects.filter(name=request.user)
			args = {'newposts':newpost , 'users':user , 'datas':data1}
			
			return render(request , 'account/profile.html', args)
		else:	
			print("error")
			user = User.objects.filter(username='171b0411')
			data1 = data.objects.filter(name=request.user)
			newpost = Createpost.objects.all().order_by('-date_posted')
			args = {'newposts':newpost  , 'users':user , 'datas':data1}
			return render(request , 'account/profile.html', args)
	else:
		user = User.objects.filter(username='171b0411')
		data1 = data.objects.filter(name=request.user)
		newpost = Createpost.objects.all().order_by('-date_posted')
		args = {'newposts':newpost  , 'users':user, 'datas':data1}
		return render(request , 'account/profile.html' , args)

def login(request):
	if(request.method=="POST"):
		print("ok")
		params=request.POST
		user=authenticate(params['username'], params['password'])
		if(user is not None):
			login(request, User.objects.get(user__username=params['username']))
			return render(request , 'account/profile.html')
		else:
			return HttpResponse("error")
	else:
		return render(request , 'account/login.html')

