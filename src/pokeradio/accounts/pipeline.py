from django.conf import settings
from pokeradio.tasks import create_image
import redis

r = redis.Redis()
def get_profile_pic(strategy, details, response, user=None, is_new=False, *args, **kwargs):

	
	user_key = "user_id_{0}".format(user.id)
	
	""" TODO: Get new image every 24 hours """
	def save_image():	
		image_url = response.get('picture','default')

		if image_url != 'default':
			user_id = str(user.id)
			r.setex(user_key, 'profile_pic', 60 * 60 * 24)
			create_image(image_url, user_id, settings.USER_PROFILE_PICTURES_BASE_DIR, settings.PROFILE_PICTURE_SIZE)
			print 'save'
			return

	
	
	user_last_pic_dl = r.get(user_key)

	if is_new or user_last_pic_dl == None :
		save_image()
		



		

	





