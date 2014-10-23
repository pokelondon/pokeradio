import requests
from PIL import Image
from StringIO import StringIO
from os import stat

from pokeradio.celeryapp import app


def create_image(imageurl, output_file, output_dir, size):
    """ Get a remote image and save a thumbnail locally,
    return the open image object
    """
    r = requests.get(imageurl)
    image = Image.open(StringIO(r.content))
    image.thumbnail(size, Image.ANTIALIAS)

    if image.mode != "RGB":
        image = image.convert("RGB")

    output_file = '{0}/{1}.jpg'.format(output_dir, output_file)
    image.save(output_file)
    statinfo = stat(output_file)

    return (image, statinfo.st_size)


@app.task
def trigger_badge_add_task(track_id):
    from pokeradio.badges import BadgeManager
    from pokeradio.models import Track
    instance = Track.objects.get(id=track_id)
    BadgeManager.trigger('add', instance)
