"""
Summarize a directory of playlists.  For now that just prints counts by artist.
"""
# pylint: disable=C0103

from collections import Counter
import json
import logging
import os
import os.path

from frozendict import frozendict

class PlaylistDir:
    """
    Processes a playlist directory.  Not thread safe, but is externally immutable if
    only the public interface is used.
    """
    def __init__(self, directory):
        self._directory = directory
        self._filenames = None
        self._items = None
        self._artist_counts = None
        self._loaded = False
        self._counted = False

    def _load(self):
        if not self._loaded:
            items = []
            filenames = []
            for name in os.listdir(self._directory):
                filename = os.path.join(self._directory, name)
                logging.info('Load %s', filename)
                filenames.append(filename)
                with open(filename, 'r') as fp:
                    items.extend([frozendict(item) for item in json.load(fp)])
            self._filenames = tuple(filenames)
            self._items = tuple(items)
            self._loaded = True

    def _count(self):
        if not self._counted:
            self._load()
            self._artist_counts = Counter()
            self._artist_counts.update([i['artist'] for i in self._items])
            self._counted = True

    @property
    def artist_counts(self):
        """ Get counts by artist """
        self._count()
        return Counter(self._artist_counts)

    @property
    def filenames(self):
        """ Get all playlist filenames from the directory """
        self._load()
        return self._filenames

    @property
    def items(self):
        """ Get all playlist items from the directory """
        self._load()
        return self._items

def _main(directory, output_fp):
    playlist_dir = PlaylistDir(directory)
    artist_counts = playlist_dir.artist_counts
    counts = [{'artist': ac[0], 'count': ac[1]} for ac in artist_counts.most_common()]
    json.dump(counts, output_fp, indent=2)

if __name__ == '__main__':
    import argparse
    logging.basicConfig(level=logging.INFO)
    arg_parser = argparse.ArgumentParser(description='Summarize playlists in a directory')
    arg_parser.add_argument('-o', '--output', default=None, help='Output file')
    arg_parser.add_argument('directory', help='Directory containing playlists')
    args = arg_parser.parse_args()

    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)

        with open(args.output, 'w', encoding='utf-8') as fp_out:
            _main(args.directory, fp_out)
    else:
        with open(1, 'w', encoding='utf-8', errors='backslashreplace', closefd=False) as fp_out:
            _main(args.directory, fp_out)
