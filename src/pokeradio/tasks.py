from PIL import Image
from StringIO import StringIO
from os import stat
import requests

def create_image(imageurl, output_file, output_dir, size):

	r = requests.get(imageurl)
	image = Image.open(StringIO(r.content))
	image.thumbnail(size, Image.ANTIALIAS)

	output_file = '{0}/{1}.jpg'.format(output_dir, output_file)
	image.save(output_file)
	statinfo = stat(output_file)

	return (image, statinfo.st_size)