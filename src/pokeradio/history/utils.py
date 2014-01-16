from pokeradio.history.models import ArchiveTrack, Artist, Play
from pokeradio.models import Track


def get_or_create_artist(track):
    """ Used by get_or_create_track, finds existing Artist object if
    available, otherwise creates one.
    """

    try:
        artist = Artist.objects.get(spotify_artist_href=track.artist_href)
    except Artist.DoesNotExist:
        artist = Artist.objects.create(spotify_artist_href=track.artist_href,
                                       name=track.artist)
    return artist


def get_or_create_track(track):
    """ Accepts a Playlist Track and looks for a record of it in the archive
    using the Spotify URI as a unique reference.
    If an ArchiveTrack cannot be found, one is created
    """

    try:
        track = ArchiveTrack.objects.get(spotify_href=track.href)
    except ArchiveTrack.DoesNotExist:
        artist = get_or_create_artist(track)
        track = ArchiveTrack.objects.create(
                spotify_href=track.href,
                name=track.name,
                spotify_album_href=track.album_href,
                length=track.length,
                artist=artist)
    return track


def record_track_play(track):
    """ Takes a Playlist Track object, and finds or creates an ArchiveTrack
    and adds a play to it against the user linked to the playlist track
    """
    archive_track = get_or_create_track(track)
    play = Play.objects.create(track=archive_track, user=track.user)
