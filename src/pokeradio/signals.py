import django.dispatch
from pokeradio.history.models import ArchiveTrack, Artist, Play


track_played = django.dispatch.Signal(providing_args=('instance', ))


def signal_track_played(sender, **kwargs):
    # Try to find the track and artist
    pass

track_played.connect(signal_track_played)
