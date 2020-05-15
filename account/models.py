from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class data(models.Model):
	name = models.ForeignKey(User, on_delete=models.CASCADE)
	dob = models.DateField()


class Profile(models.Model):
	user = models.OneToOneField(User ,on_delete=models.CASCADE)	
	image = models.ImageField(default='default.jpg',upload_to='profile_pics')

	def __str__(self):
		return f'{self.user}'




class Comments(models.Model):
	user=models.ForeignKey(Profile, on_delete=models.CASCADE)
	commentData=models.TextField(blank=True, null=True)
	postedOn=models.DateTimeField(auto_now=True)


class Createpost(models.Model):
	content = models.CharField(max_length=100)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date_posted = models.DateTimeField(default=timezone.now)
	comments=models.ManyToManyField(Comments, blank=True)

	def __str__(self):
		return 	f'{self.user}'


class Notifications(models.Model):
	fromUser=models.ForeignKey(User , related_name='sender',on_delete=models.CASCADE)
	toUser=models.ForeignKey(User , related_name='receiver',on_delete=models.CASCADE)
	
	created=models.DateTimeField(default=timezone.now)

class FriendFormation(models.Model):
	fromUser=models.ForeignKey(User , related_name='friendOwner',on_delete=models.CASCADE)
	toUser=models.ForeignKey(User , related_name='friendReceiver',on_delete=models.CASCADE)
	isFriend=models.BooleanField(default=False)
	isFriendRequest=models.BooleanField(default=True)
	created=models.DateTimeField(auto_now=True)


class Friend(models.Model):
	users = models.ManyToManyField(FriendFormation, blank=True)
	current_user = models.ForeignKey(User , related_name='owner',null=True,on_delete=models.CASCADE)

	@classmethod
	def add_request(self, current_user,new_friend):
		if(FriendFormation.objects.filter(fromUser=current_user, toUser=new_friend).count()==0):
			obj, notif = FriendFormation.objects.get_or_create(fromUser=current_user, toUser=new_friend)
			if(notif):
				obj.save()
				
				if(Friend.objects.filter(current_user=new_friend).count()==0):
					friend, notif = self.objects.get_or_create(current_user=new_friend)
					friend.save()
		else:
			pass


	@classmethod
	def accept_request(self, current_user,new_friend):
		if(FriendFormation.objects.filter(fromUser=new_friend, toUser=current_user).count()>0):
			obj = FriendFormation.objects.get(fromUser=new_friend, toUser=current_user)
			obj.isFriendRequest=False
			obj.isFriend=True
			obj.save()
			friend = self.objects.get(current_user=current_user)
			friend1 = self.objects.get(current_user=new_friend)
			friend.users.add(obj)
			friend1.users.add(obj)
			p , obj1 = Notifications.objects.get_or_create(fromUser=new_friend,toUser=current_user)
			p.save()

		else:
			obj = FriendFormation.objects.get(fromUser=current_user, toUser=new_friend)
			obj.isFriendRequest=False
			obj.isFriend=True
			obj.save()
			friend = self.objects.get(current_user=current_user)
			friend1 = self.objects.get(current_user=new_friend)
			friend.users.add(obj)
			friend1.users.add(obj)

	@classmethod
	def reject_request(self, current_user,new_friend):
		if(FriendFormation.objects.filter(fromUser=current_user, toUser=new_friend).count()>0):
			FriendFormation.objects.get(fromUser=current_user, toUser=new_friend).delete()
		else:
			FriendFormation.objects.get(fromUser=new_friend, toUser=current_user).delete()

	@classmethod
	def cancel_request(self, current_user,new_friend):
		FriendFormation.objects.get(fromUser=current_user, toUser=new_friend).delete()


	@classmethod
	def lose_friend(self, current_user,new_friend):
		if(FriendFormation.objects.filter(fromUser=current_user, toUser=new_friend).count()>0):
			FriendFormation.objects.get(fromUser=current_user, toUser=new_friend).delete()
			Notifications.objects.get(fromUser=current_user,toUser=new_friend).delete()
		elif(FriendFormation.objects.filter(fromUser=new_friend, toUser=current_user).count()>0):
			FriendFormation.objects.get(fromUser=new_friend, toUser=current_user).delete()
			Notifications.objects.get(fromUser=new_friend,toUser=current_user).delete()



