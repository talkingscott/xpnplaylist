"""
Get the XPN playlist page for a date and parse it to a list of dict.
"""
# pylint: disable=C0103

from html.parser import HTMLParser
from html.entities import name2codepoint
import json
import logging
import os
import os.path
import traceback

import requests

DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

PLAYLIST_URL = 'http://xpn.org/playlists/xpn-playlist'

def _attr(attrs, attr_name):
    """ Gets the value of an attribute or None """
    for attr in attrs:
        if attr[0] == attr_name:
            return attr[1]
    return None

def _days_in_month(month_0, year):
    """ Returns days in a month (0-indexed).  Hope I got this right. """
    if month_0 != 1:
        return DAYS_IN_MONTH[month_0]
    if (year % 4) == 0 and ((year % 100) != 0 or (year % 400) == 0):
        return DAYS_IN_MONTH[month_0] + 1
    return DAYS_IN_MONTH[month_0]

def _reformat_date_for_post(date):
    """ Reformats a date string from yyyy-MM-dd to MM-dd-yyyy """
    return date[5:] + '-' + date[:4]

def _reformat_time(time):
    """ Reformats a time string from hh:mm am to HH:mm """
    hour = time[:2]
    ampm = time[6:]
    if hour == '12':
        if ampm == 'am':
            hour = '00'
        else:
            hour = '12'
    else:
        if ampm == 'pm':
            hour = str(int(hour) + 12)
    return hour + ':' + time[3:5]

def _parse_item(data):
    """ Parses an item from the playlist or None for programming or support requests """
    if data.startswith("Like what you're hearing?"):
        return None
    if len(data) < 10:
        logging.info('Short item: %r length: %d', data, len(data))
        return None
    if data[9] == '|':
        return None
    time = _reformat_time(data[:8])
    try:
        artist, track = data[9:].split(' - ', 1)
    except: # pylint: disable=W0702
        logging.error('Splitting %s: %s', data, traceback.format_exc())
        return None
    return {
        'time': time,
        'artist': artist,
        'track': track
    }

class PlaylistParser(HTMLParser):   # pylint: disable=R0902
    """ Parses a playlist from xpn.org HTML """
    def __init__(self, date):
        super().__init__()
        self._date = date
        self._playlist = []
        self._depth = 0
        self._have_article_body = False
        self._have_accordian_resized = False
        self._have_accordian = False
        self._get_item = False
        self._done = False
        self._previous_item = {}

    @property
    def playlist(self):
        """ The playlist parsed from HTML """
        return self._playlist

    def handle_starttag(self, tag, attrs):
        if self._done:
            return
        if not self._have_article_body:
            if tag == 'div' and _attr(attrs, 'itemprop') == 'articleBody':
                logging.debug('Have articleBody')
                self._have_article_body = True
            return
        if not self._have_accordian_resized:
            if tag == 'div' and _attr(attrs, 'id') == 'accordion-resizer':
                logging.debug('Have accordion-resizer')
                self._have_accordian_resized = True
                self._depth = 1
            return
        self._depth += 1
        if not self._have_accordian:
            if tag == 'div' and _attr(attrs, 'id') == 'accordion':
                logging.debug('Have accordion')
                self._have_accordian = True
            return
        if tag == 'a':
            logging.debug('Have anchor')
            self._get_item = True

    def handle_endtag(self, tag):
        if self._done:
            return
        if self._have_accordian_resized:
            self._depth -= 1
            if self._depth <= 0:
                logging.debug('Done')
                self._done = True

    def handle_data(self, data):
        if self._done:
            return
        if self._get_item:
            logging.debug('Possible item: %s', data)
            item = _parse_item(data)
            if item and item != self._previous_item:
                self._previous_item = item.copy()
                item['datetime'] = self._date + ' ' + item['time']
                item['date'] = self._date
                self._playlist.append(item)
            self._get_item = False

    def handle_comment(self, data):
        logging.debug("Comment: %s", data)

    def handle_entityref(self, name):
        ch = chr(name2codepoint[name])
        logging.info("Named entity: %s", ch)

    def handle_charref(self, name):
        if name.startswith('x'):
            ch = chr(int(name[1:], 16))
        else:
            ch = chr(int(name))
        logging.info("Numeric entity: %s", ch)

    def handle_decl(self, decl):
        logging.debug("Decl: %s", decl)

    def error(self, message):
        logging.error(message)

def get_playlist_for(playlist_date):
    """ Gets the playlist for a date """
    parser = PlaylistParser(playlist_date)
    resp = requests.post(PLAYLIST_URL,
                         data={'playlistdate': _reformat_date_for_post(playlist_date)})
    parser.feed(resp.text)
    parser.close()
    return parser.playlist

def write_playlist_for(playlist_date, directory):
    """ Writes a playlist for a date to a file """
    playlist = get_playlist_for(playlist_date)
    filename = os.path.join(directory, f'playlist-{playlist_date}.json')
    with open(filename, 'w') as fp:
        fp.write(json.dumps(playlist, indent=2))
    logging.info('Wrote %d playlist items to %s', len(playlist), filename)

def _dates_for_date(date):
    if len(date) == 10:
        yield date
    elif len(date) == 7:
        month0 = int(date[5:]) - 1
        year = int(date[:4])
        for day0 in range(_days_in_month(month0, year)):
            yield date + '-' + ('%02d' % (day0 + 1))
    elif len(date) == 4:
        year = int(date)
        for month0 in range(12):
            for day0 in range(_days_in_month(month0, year)):
                yield date + '-' + ('%02d' % (month0 + 1)) + '-' + ('%02d' % (day0 + 1))

if __name__ == '__main__':
    import argparse

    logging.basicConfig(level=logging.INFO)

    arg_parser = argparse.ArgumentParser(description='Get XPN Playlists')
    arg_parser.add_argument('-D', '--directory', default='.', help='The directory for output')
    arg_parser.add_argument('date', nargs='+',
                            help='The date(s) to fetch (yyyy-MM-dd or yyyy-MM or yyyy)')
    args = arg_parser.parse_args()

    try:
        os.makedirs(args.directory)
    except IOError:
        pass

    for _date in args.date:
        for play_date in _dates_for_date(_date):
            write_playlist_for(play_date, args.directory)
