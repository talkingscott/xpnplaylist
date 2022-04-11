"""
Get a playlist from a radio/streaming service for one or more dates.

The playlist for each date is written to a separate file as a JSON array of
objects.
"""
import argparse
import collections.abc
import json
import logging
import os
import os.path
import sys
import time
from typing import Any, Mapping, Optional, Sequence, Union

import requests

from lib.dates import dates_for_datespec

NativeJson = Optional[Union[Sequence[Mapping[str, str]], Mapping[str, Any]]]
PlaylistJson = Optional[Sequence[Mapping[str, str]]]


def get_playlist_native_json(playlist_url: str, playlist_date: str) -> NativeJson:
    """Get a playlist as the JSON native to the service."""
    epoch_millis = int(time.time() * 1000)
    playlist_date_slashes = playlist_date.replace("-", "/")
    url = playlist_url.format(
        epoch_millis=epoch_millis,
        playlist_date=playlist_date,
        playlist_date_slashes=playlist_date_slashes
    )
    resp = requests.get(url)
    if resp.status_code >= 400:
        logging.error(
            "Error getting data for %s: %d",
            playlist_date,
            resp.status_code
        )
        if resp.status_code >= 500:
            time.sleep(1)
            resp = requests.get(url)
            if resp.status_code >= 400:
                logging.error(
                    "Error in second try getting data for %s: %d",
                    playlist_date,
                    resp.status_code
                )
                return None
            logging.info("Retry successful for %s", playlist_date)
        else:
            return None

    content_type = resp.headers["content-type"]
    if not content_type.startswith("application/json"):
        logging.error("Got %s instead of JSON for %s", content_type, playlist_date)
        return None

    logging.debug("Response: %s", resp.text)
    return resp.json()


class KCRWPlaylistFetcher:
    """Fetch and parse KCRW playlists."""
    def __init__(self):
        self.url = "https://tracklist-api.kcrw.com/Simulcast/date/{playlist_date_slashes}"

    def get_playlist(self, playlist_date: str) -> PlaylistJson:
        """Get a KCRW playlist in our format."""
        playlist = get_playlist_native_json(self.url, playlist_date)
        if not playlist:
            return None
        if not isinstance(playlist, collections.abc.Sequence):
            logging.error("Unexpected data structure for %s", playlist_date)
            return None
        return [self._parse_item(item) for item in filter(self._keep_item, playlist)]

    def _date_parts_for_item(self, item: Mapping[str, str]):
        if isinstance(item["datetime"], str):
            played_at = item["datetime"]
            date = played_at[:10]
            tod = played_at[11:19]
        else:
            date = item["date"]
            tod = "00:00"
        datetime = f"{date} {tod}"
        return datetime, date, tod

    def _keep_item(self, item: Mapping[str, str]):
        return item["title"] and not item["artist"] == "[BREAK]"

    def _parse_item(self, item: Mapping[str, str]):
        """Parses an item from a KCRW playlist."""
        datetime, date, tod = self._date_parts_for_item(item)
        return {
            "time": tod,
            "artist": item["artist"],
            "track": item["title"],
            "date": date,
            "datetime": datetime,
            "album": item["album"]
        }


class TheCurrentPlaylistFetcher:
    """Fetch and parse The Current playlists."""
    def __init__(self):
        self.url = "https://www.thecurrent.org/_next/data/4Fb9cdLRrYDReTyiEcTtA/playlist/the-current/{playlist_date}.json?slug=the-current&slug={playlist_date}"

    def get_playlist(self, playlist_date: str) -> PlaylistJson:
        """Get a The Current playlist in our format."""
        playlist = get_playlist_native_json(self.url, playlist_date)
        if not playlist:
            return None
        if not isinstance(playlist, collections.abc.Mapping):
            logging.error("Unexpected data structure for %s", playlist_date)
            return None
        return [self._parse_item(item) for item in playlist["pageProps"]["data"]["songs"]]

    def _date_parts_for_item(self, item: Mapping[str, str]):
        played_at = item["played_at"]
        date = played_at[:10]
        tod = played_at[11:19]
        datetime = f"{date} {tod}"
        return datetime, date, tod

    def _parse_item(self, item: Mapping[str, str]):
        """Parse an item from a The Current playlist."""
        datetime, date, tod = self._date_parts_for_item(item)
        return {
            "time": tod,
            "artist": item["artist"],
            "track": item["title"],
            "date": date,
            "datetime": datetime,
            "album": item["album"]
        }


class WNCWPlaylistFetcher:
    """Fetch and parse WNCW playlists."""
    def __init__(self):
        self.url = "https://api.composer.nprstations.org/v1/widget/5187f56de1c8c6a808e91b8d/playlist?t={epoch_millis}&datestamp={playlist_date}&order=1&errorMsg=No+results+found.+Please+modify+your+search+and+try+again."

    def get_playlist(self, playlist_date: str) -> PlaylistJson:
        """Get a WNCW playlist in our format."""
        playlist = get_playlist_native_json(self.url, playlist_date)
        if not playlist:
            return None
        if not isinstance(playlist, collections.abc.Mapping):
            logging.error("Unexpected data structure for %s", playlist_date)
            return None
        return [self._parse_item(item) for plist in playlist["playlist"] for item in filter(self._keep_item, plist["playlist"])]

    def _date_parts_for_item(self, item: Mapping[str, str]):
        datetime = item["_start_time"]
        date = datetime[:10]
        tod = datetime[11:19]
        datetime = f"{date} {tod}"
        return datetime, date, tod

    def _keep_item(self, item: Mapping[str, str]):
        return "artistName" in item

    def _parse_item(self, item: Mapping[str, str]):
        """Parse an item from a The Current playlist."""
        datetime, date, tod = self._date_parts_for_item(item)
        return {
            "time": tod,
            "artist": item["artistName"],
            "track": item["trackName"],
            "date": date,
            "datetime": datetime,
            "album": item.get("collectionName")
        }


class XPNPlaylistFetcher:
    """Fetch and parse XPN playlists."""
    DATETIME_KEYS = ("air_date", "timeslice")

    def __init__(self, service: str):
        if service == "xpn":
            self.url = "https://origin.xpn.org/utils/playlist/json/{playlist_date}.json"
        else:
            self.url = "https://origin.xpn.org/xpn2/json/{playlist_date}.json"

    def get_playlist(self, playlist_date: str) -> PlaylistJson:
        """Get an XPN playlist in our format."""
        playlist = get_playlist_native_json(self.url, playlist_date)
        if not playlist:
            return None
        if not isinstance(playlist, collections.abc.Sequence):
            logging.error("Unexpected data structure for %s", playlist_date)
            return None
        return [self._parse_item(item) for item in filter(self._keep_item, playlist)]

    def _date_parts_for_item(self, item: Mapping[str, str]):
        for key in self.DATETIME_KEYS:
            if key in item:
                datetime = item[key]
                parts = datetime.split(" ")
                return datetime, parts[0], parts[1]
        raise ValueError("No time found: %s" % json.dumps(item, indent=2))

    def _keep_item(self, item: Mapping[str, str]):
        return not item["artist"].startswith("|")

    def _parse_item(self, item: Mapping[str, str]):
        """Parse an item from an XPN playlist."""
        datetime, date, tod = self._date_parts_for_item(item)
        return {
            "time": tod,
            "artist": item["artist"],
            "track": item["song"],
            "date": date,
            "datetime": datetime,
            "album": item["album"]
        }


def write_playlist(fetcher, playlist_date: str, directory: str):
    """Fetch and write a playlist for a date to a file."""
    playlist = fetcher.get_playlist(playlist_date)
    if playlist:
        filename = os.path.join(directory, f'playlist-{playlist_date}.json')
        with open(filename, 'w') as pfp:
            pfp.write(json.dumps(playlist, indent=2))
        logging.info('Wrote %d playlist items to %s', len(playlist), filename)
    else:
        logging.info("Nothing written for %s", playlist_date)


def main():
    """Write a playlist file for each date specified on the command line."""
    logging.basicConfig(
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        level=logging.INFO
    )

    arg_parser = argparse.ArgumentParser(description='Get XPN Playlists')
    arg_parser.add_argument(
        '-D',
        '--directory',
        help='The directory for output'
    )
    arg_parser.add_argument(
        '-S',
        '--service',
        default='xpn',
        help='The service (xpn|xpn2|thecurrent|kcrw|wncw)'
    )
    arg_parser.add_argument(
        'date',
        nargs='+',
        help='The date(s) to fetch (yyyy-MM-dd or yyyy-MM or yyyy)'
    )
    args = arg_parser.parse_args()

    if args.service in ("xpn", "xpn2"):
        fetcher = XPNPlaylistFetcher(args.service)
    elif args.service == "thecurrent":
        fetcher = TheCurrentPlaylistFetcher()
    elif args.service == "kcrw":
        fetcher = KCRWPlaylistFetcher()
    elif args.service == "wncw":
        fetcher = WNCWPlaylistFetcher()
    else:
        logging.fatal("Unknown service: %s", args.service)
        sys.exit(1)

    try:
        os.makedirs(args.directory)
    except IOError:
        pass

    if args.directory:
        output_dir = args.directory
    else:
        output_dir = os.path.join("playlists", args.service, args.date[0][:4])

    for _date in args.date:
        for play_date in dates_for_datespec(_date):
            write_playlist(fetcher, play_date, output_dir)


if __name__ == '__main__':
    main()
