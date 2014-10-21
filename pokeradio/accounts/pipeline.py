from django.conf import settings
from pokeradio.tasks import create_image

def get_profile_pic(strategy, details, response, user=None, is_new=False, *args, **kwargs):
	
	""" TODO: Get new image every 24 hours """
	def save_image():	
		image_url = response.get('picture','default')

		if image_url != 'default':
			user_id = str(user.id)
			create_image(image_url, user_id, settings.USER_PROFILE_PICTURES_BASE_DIR, settings.PROFILE_PICTURE_SIZE)

	save_image()
		



		

	





