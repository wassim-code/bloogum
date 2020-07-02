from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Post(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField(max_length=4000)
	pub_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	views = models.IntegerField(default=0)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post_detail', kwargs={'pk': self.pk})

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	img = models.ImageField(default='default.jpg', upload_to='profile_pics')

	def __str__(self):
		return f"{self.user.username} profile"

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	pub_date = models.DateTimeField(auto_now_add=True)
	content = models.TextField(max_length=4000)
	
	def __str__(self):
		return self.content[:20]

	def get_absolute_url(self):
		return reverse('post_detail', kwargs={'pk': self.post.pk})

class Email(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_emails')
    sent_tm = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=4000)

    def __str__(self):
    	return self.subject

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()