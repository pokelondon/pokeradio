from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import redis


class Track(models.Model):
	name = models.CharField(max_length = 255)
	artist = models.CharField(max_length = 255)
	href = models.CharField(max_length = 255)
	timestamp = models.DateTimeField(auto_now_add = True)
	played = models.BooleanField(default = False)
	user = models.ForeignKey(User)
	"""TODO: 
	Add validation that prevents user from chossing the same song multiple times in the a timeframe 
	"""
	class Meta:
		ordering = ['timestamp']


@receiver(post_save, sender=Track)
def track_saved(sender, **kwargs):
	print 'SAVED!!'
	r = redis.Redis()
	r.publish('playlist_changed', 'SAVED')

@receiver(post_delete, sender=Track)
def track_deleted(sender, **kwargs):
	print 'Deleted!!'
	r = redis.Redis()
	r.publish('playlist_changed', 'DELETE')




