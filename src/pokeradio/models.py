from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from calendar import timegm
import simplejson as json
import redis


class Track(models.Model):
	name = models.CharField(max_length = 255)
	artist = models.CharField(max_length = 255)
	href = models.CharField(max_length = 255)
	timestamp = models.DateTimeField(auto_now_add = True)
	played = models.BooleanField(default = False)
	user = models.ForeignKey(User)
	length = models.FloatField(null=True)
	"""TODO: 
	Add validation that prevents user from chossing the same song multiple times in the a timeframe 
	"""

	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name,
			'artist': self.artist,
			'href': self.href,
			'timestamp': timegm(self.timestamp.utctimetuple()),
			'played': self.played,
			'length': self.length,
			'user_fullname': self.user.get_full_name()
		}
		

	class Meta:
		ordering = ['timestamp']


@receiver(post_save, sender=Track)
def track_saved(sender, instance, **kwargs):
	r = redis.Redis()
	r.publish('playlist', json.dumps(instance.to_dict()))

@receiver(post_delete, sender=Track)
def track_deleted(sender, **kwargs):
	print 'Deleted!!'
	r = redis.Redis()
	r.publish('playlist_changed', 'DELETED')




