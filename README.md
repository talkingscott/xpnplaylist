# XPN Playlist Acquisition and Summarization

[WXPN](http://xpn.org) is a radio station from the University of Pennsylvania in Philadelphia.  Their daily playlists are available on their web site back to 2007-01-19.  My curiosity about whether they *ever* played [Eliza Doolittle](https://www.elizalovechild.com/) led me to write the scripts here.

## Scripts

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
```

## Results

I tabulated annual totals for some artists I like, but never seem to hear, along with a few "similar" artists that I do hear.  Note that K.T. Tunstall is spelled multiple ways in the playlists.  I did not aggregate across the spellings.

| artist | 2007 | 2008 | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 |
| ------ | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| bitter:sweet | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| dido | 2 | 2 | 51 | 61 | 66 | 55 | 58 | 40 | 20 | 21 | 14 | 22 |
| eliza doolittle | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| fatboy slim | 28 | 16 | 33 | 12 | 50 | 38 | 16 | 18 | 8 | 11 | 12 | 14 |
| feist | 4 | 116 | 1 | 104 | 429 | 294 | 129 | 123 | 48 | 47 | 76 | 52 |
| ingrid michaelson | 1 | 1 | 1 | 378 | 176 | 361 | 124 | 1 | 68 | 62 | 38 | 49 |
| jem | 35 | 11 | 28 | 28 | 26 | 24 | 19 | 10 | 8 | 2 | 4 | 1 |
| k. t. tunstall | 0 | 66 | 70 | 286 | 210 | 98 | 240 | 104 | 54 | 58 | 44 | 151 |
| k.t. tunstall | 420 | 114 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| kt tunstall | 1 | 3 | 1 | 20 | 3 | 6 | 20 | 2 | 0 | 0 | 1 | 2 |
| kate bush | 2 | 1 | 1 | 111 | 126 | 99 | 85 | 91 | 64 | 53 | 71 | 87 |
| lana del rey | 0 | 0 | 0 | 0 | 105 | 394 | 139 | 450 | 152 | 94 | 220 | 119 |
| lenka | 0 | 6 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| lily allen | 17 | 2 | 257 | 99 | 88 | 70 | 50 | 49 | 19 | 17 | 19 | 21 |
| material | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| paramore | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| regina spektor | 2 | 1 | 1 | 154 | 50 | 241 | 66 | 48 | 16 | 22 | 15 | 4 |
| sara bareilles | 3 | 78 | 1 | 44 | 64 | 36 | 28 | 26 | 11 | 12 | 9 | 44 |
| sia | 4 | 6 | 17 | 25 | 24 | 19 | 17 | 10 | 3 | 5 | 5 | 7 |
| sofi tukker | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 | 0 | 0 |
| the crystal method | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| thievery corporation | 5 | 24 | 199 | 53 | 47 | 32 | 47 | 71 | 21 | 25 | 25 | 16 |
