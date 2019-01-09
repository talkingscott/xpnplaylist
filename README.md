# XPN Playlist Acquisition and Summarization

[WXPN](http://xpn.org) is a radio station from the University of Pennsylvania in Philadelphia.  Their daily playlists are available on their web site back to 2007-01-19.  My curiosity about whether they *ever* played [Eliza Doolittle](https://www.elizalovechild.com/) led me to write the scripts here.

The get_playlist.py script downloads daily playlists as JSON.  It accepts partial dates, so that 2018-03-15 specifies a single day, 2018-03 specifies all days in that month, and 2018 specifies all days in that year.  The script also accepts an optional directory argument.

```bash
$ pipenv run get_playlist.py --help
usage: get_playlist.py [-h] [-D DIRECTORY] date [date ...]

Get XPN Playlists

positional arguments:
  date                  The date(s) to fetch (yyyy-MM-dd or yyyy-MM or yyyy)

optional arguments:
  -h, --help            show this help message and exit
  -D DIRECTORY, --directory DIRECTORY
                        The directory for output

$ pipenv run get_playlist.py playlists/2018 2018-11-29 2018-11-30 2018-12
```

The summarize_playlists.py script reads a directory of downloaded playlists and prints a summary, which at this time is simply a count by artist.

```bash
$ pipenv run summarize_playlists.py --help
usage: summarize_playlists.py [-h] [-o OUTPUT] directory

Summarize playlists in a directory

positional arguments:
  directory             Directory containing playlists

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file

$ pipenv run summarize_playlists.py -o counts-2018.txt playlists/2018
