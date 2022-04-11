"""Count artists and tracks for each service."""
import collections
import collections.abc
import glob
import json
import logging


def _count_artists_and_tracks_in_playlist(filename):
    artists = collections.Counter()
    tracks = collections.Counter()
    with open(filename, "r", encoding="utf-8") as pfp:
        playlist = json.load(pfp)
        if not isinstance(playlist, collections.abc.Sequence):
            logging.warning("Non-list read from %s", filename)
            return artists, tracks
        for item in playlist:
            if item["artist"] and item["track"]:
                artist = item["artist"].lower()
                artists.update((artist,))
                tracks.update((item["track"].lower() + "\t" + artist,))
        return artists, tracks


def _main():
    logging.basicConfig(
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        level=logging.DEBUG
    )

    services = ("kcrw", "thecurrent", "wncw", "xpn", "xpn2")

    for service in services:
        logging.info("Calculate counts for %s", service)

        artists = collections.Counter()
        tracks = collections.Counter()

        for path in glob.iglob(f"playlists/{service}/*/*.json"):
            logging.debug("Calculate counts for %s", path)
            arts, trks = _count_artists_and_tracks_in_playlist(path)
            artists.update(arts)
            tracks.update(trks)

        with open(f"counts/{service}-artist-counts.txt", "w", encoding="utf-8") as afp:
            for artist, count in artists.most_common():
                print(f"{artist}\t{count}", file=afp)

        with open(f"counts/{service}-track-counts.txt", "w", encoding="utf-8") as tfp:
            for track, count in tracks.most_common():
                print(f"{track}\t{count}", file=tfp)


if __name__ == "__main__":
    _main()
