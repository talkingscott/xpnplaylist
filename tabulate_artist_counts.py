"""
Tabulate playlist counts for artists.  Uses counts files already created by summarize_playlists.py.
"""
# pylint: disable=invalid-name

from collections import Counter
import json
import os.path
import sys

from lib.artists import canonical_name

class CountsDir:
    """ Operations on a directory of annual counts by artist """
    def __init__(self, directory):
        self._directory = directory
        self._years = list(range(2007, 2022))
        self._artist_total_counts = Counter()
        self._artist_counts = {}
        self._artists = set()
        self._artist_tuple = ()

    def load_artist_counts(self):
        """ Loads artist counts. """
        for i, year in enumerate(self._years):
            filename = os.path.join(self._directory, f'count-{str(year)}.json')
            with open(filename) as fp:
                counts = json.load(fp)
                for ac in counts:
                    artist = canonical_name(ac['artist'])
                    if artist in self._artists:
                        self._artist_counts[artist][i] += ac['count']

    def load_artist_total_counts(self):
        """ Loads total counts. """
        self._artist_total_counts = Counter()
        for year in self._years:
            filename = os.path.join(self._directory, f'count-{str(year)}.json')
            with open(filename) as fp:
                artist_counts = json.load(fp)
                for artist_count in artist_counts:
                    artist = canonical_name(artist_count['artist'])
                    self._artist_total_counts[artist] += artist_count['count']

    def load_artists(self, artists):
        """ Loads artists from a list. """
        self._artist_counts = {}
        self._artists = set()
        for artiste in artists:
            artist = canonical_name(artiste)
            self._artist_counts[artist] = [0] * len(self._years)
            self._artists.add(artist)
        self._artist_tuple = tuple(artists)

    def load_artists_file(self, filename):
        """ Loads artists from a file. """
        with open(filename) as fp:
            self._artist_counts = {}
            self._artists = set()
            artist_list = []
            for line in fp:
                artist = canonical_name(line.strip())
                self._artist_counts[artist] = [0] * len(self._years)
                self._artists.add(artist)
                artist_list.append(artist)
            self._artist_tuple = tuple(artist_list)

    @property
    def artists(self):
        """
        Returns the artists.
        """
        return self._artist_tuple

    @property
    def artist_counts(self):
        """
        Gets artist counts.  N.B. because this returns the underlying arrays, the caller
        can mutate state.
        """
        return self._artist_counts.copy()

    @property
    def artist_total_counts(self):
        """
        Gets artist overall counts.
        """
        return self._artist_total_counts.copy()

    @property
    def directory(self):
        """ Gets the directory with counts. """
        return self._directory

    @property
    def years(self):
        """ Gets the years. """
        return tuple(self._years)

def _write_counts_tsv(counts_dir, fp):
    """ write the artist counts as tab-separated values with a header. """
    print('artist\t' + '\t'.join(map(str, counts_dir.years)), file=fp)
    for artist, counts in counts_dir.artist_counts.items():
        print(artist + '\t' + '\t'.join(map(str, counts)), file=fp)

def _write_counts_md(counts_dir, fp):
    """ write the artist counts as a markdown table. """
    print('| artist | ' + ' | '.join(map(str, counts_dir.years)) + ' |', file=sys.stderr)
    print('| ------ | ' + ' | '.join(map(lambda y: '----', counts_dir.years)) + ' |',
          file=fp)
    for artist, counts in counts_dir.artist_counts.items():
        print('| ' + artist + ' | ' + ' | '.join(map(str, counts)) + ' |', file=fp)

def _main1():
    counts_dir = CountsDir('playlist-counts')

    counts_dir.load_artists_file('artists.txt')
    counts_dir.load_artist_counts()

    _write_counts_tsv(counts_dir, sys.stdout)
    _write_counts_md(counts_dir, sys.stderr)

def _main2():
    counts_dir = CountsDir('playlist-counts')

    counts_dir.load_artist_total_counts()

    counts_dir.load_artists([ac[0] for ac in counts_dir.artist_total_counts.most_common(26)])
    counts_dir.load_artist_counts()

    _write_counts_tsv(counts_dir, sys.stdout)
    _write_counts_md(counts_dir, sys.stderr)

def _main3():
    counts_dir = CountsDir('playlist-counts')

    counts_dir.load_artist_total_counts()

    artist_counts = []
    for artist, count in counts_dir.artist_total_counts.most_common():
        artist_counts.append({'artist': artist, 'count': count})

    print(json.dumps(artist_counts, indent=2), file=sys.stderr)

if __name__ == '__main__':
    # Modes
    # 1. Write yearly totals for artists listed in artists.txt
    # 2. Write yearly totals for overall most popular artists
    # 3. Write overall artist counts
    _main1()
