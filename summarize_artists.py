"""
Count tracks for an artist.
"""
# pylint: disable=C0103

from collections import Counter
import json
import logging
import os
import os.path

class PlaylistDir:
    """
    Operations on a directory of playlists.  This is not thread-safe, nor is it completely
    externally immutable.
    """
    def __init__(self, directory, artists):
        self._directory = directory
        self._artists = set()
        self._artist_track_counts = {}
        for artist in artists:
            lc_artist = artist.lower()
            self._artists.add(lc_artist)
            self._artist_track_counts[lc_artist] = Counter()
        self._loaded = False

    def _load(self):
        if not self._loaded:
            logging.debug('Load playlists from %s', self._directory)
            for name in os.listdir(self._directory):
                filename = os.path.join(self._directory, name)
                with open(filename, 'r') as fp:
                    items = json.load(fp)
                    for item in items:
                        artist = item['artist'].lower()
                        if artist in self._artists:
                            self._artist_track_counts[artist][item['track']] += 1
            self._loaded = True

    @property
    def artists(self):
        """ The artists being summarized """
        return set(self._artists)

    @property
    def directory(self):
        """ The directory containing playlists """
        return self._directory

    @property
    def artist_track_counts(self):
        """ N.B. This still allows Counters to be monkeyed with """
        self._load()
        return self._artist_track_counts.copy()

def _main(directory, artists):
    playlist_dir = PlaylistDir(directory, artists)
    artist_track_counts = []
    for artist, counts in playlist_dir.artist_track_counts.items():
        artist_track_count = {
            'artist': artist,
            'track_counts': [{'track': mc[0], 'count': mc[1]} for mc in counts.most_common()]
        }
        artist_track_counts.append(artist_track_count)
    print(json.dumps(artist_track_counts, indent=2))

if __name__ == '__main__':
    import argparse

    arg_parser = argparse.ArgumentParser(description='Summarize playlists for artist(s)')
    arg_parser.add_argument('-D', '--directory', default='.', help='Directory containing playlists')
    arg_parser.add_argument('artists', nargs='+', help='Artist(s)')
    args = arg_parser.parse_args()

    _main(args.directory, args.artists)
