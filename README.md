# XPN Playlist Acquisition and Summarization

[WXPN](http://xpn.org) is a radio station from the University of Pennsylvania in Philadelphia.  Their daily playlists are available on their web site back to 2007-01-19.  My curiosity about whether they *ever* played [Eliza Doolittle](https://www.elizalovechild.com/) led me to write the scripts here.

## Scripts

The get_playlist.py script downloads daily playlists as JSON.  It accepts partial dates, so that 2018-03-15 specifies a single day, 2018-03 specifies all days in that month, and 2018 specifies all days in that year.  The script also accepts an optional directory argument.

```bash
$ pipenv run get_playlist --help
usage: get_playlist.py [-h] [-D DIRECTORY] date [date ...]

Get XPN Playlists

positional arguments:
  date                  The date(s) to fetch (yyyy-MM-dd or yyyy-MM or yyyy)

optional arguments:
  -h, --help            show this help message and exit
  -D DIRECTORY, --directory DIRECTORY
                        The directory for output

$ pipenv run get_playlist playlists/2018 2018-11-29 2018-11-30 2018-12
```

The summarize_playlists.py script reads a directory of downloaded playlists and prints a summary, which at this time is simply a count by artist.

```bash
$ pipenv run summarize_playlists --help
usage: summarize_playlists.py [-h] [-o OUTPUT] directory

Summarize playlists in a directory

positional arguments:
  directory             Directory containing playlists

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file

$ pipenv run summarize_playlists -o playlist-counts/count-2018.txt playlists/2018
```

## Results

I tabulated annual totals for some artists I like, but never seem to hear, along with a few "similar" artists that I do hear.

| artist | 2007 | 2008 | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 |
| ------ | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| bitter:sweet | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| dido | 38 | 82 | 51 | 61 | 66 | 55 | 58 | 40 | 20 | 21 | 14 | 22 |
| eliza doolittle | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| fatboy slim | 28 | 34 | 33 | 12 | 50 | 38 | 16 | 18 | 8 | 11 | 12 | 14 |
| feist | 732 | 364 | 102 | 104 | 429 | 294 | 129 | 123 | 48 | 47 | 76 | 52 |
| ingrid michaelson | 162 | 413 | 412 | 378 | 176 | 361 | 124 | 805 | 68 | 62 | 38 | 49 |
| jem | 35 | 37 | 28 | 28 | 26 | 24 | 19 | 10 | 8 | 2 | 4 | 1 |
| joss stone | 425 | 102 | 158 | 89 | 184 | 218 | 112 | 86 | 119 | 46 | 34 | 48 |
| k. t. tunstall | 430 | 183 | 71 | 306 | 213 | 104 | 260 | 106 | 54 | 58 | 45 | 153 |
| kate bush | 81 | 74 | 101 | 111 | 126 | 99 | 85 | 91 | 64 | 53 | 71 | 87 |
| lana del rey | 0 | 0 | 0 | 0 | 105 | 394 | 139 | 450 | 152 | 94 | 220 | 119 |
| lenka | 0 | 6 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| lily allen | 377 | 141 | 257 | 99 | 88 | 70 | 50 | 49 | 19 | 17 | 19 | 21 |
| material | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| paramore | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| regina spektor | 190 | 40 | 311 | 154 | 50 | 241 | 66 | 48 | 16 | 22 | 15 | 4 |
| sara bareilles | 13 | 157 | 37 | 44 | 64 | 36 | 28 | 26 | 11 | 12 | 9 | 44 |
| sia | 16 | 21 | 17 | 25 | 24 | 19 | 17 | 10 | 3 | 5 | 5 | 7 |
| sofi tukker | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 | 0 | 0 |
| the crystal method | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| thievery corporation | 53 | 174 | 199 | 53 | 47 | 32 | 47 | 71 | 21 | 25 | 25 | 16 |

I also tabulated annual totals for the 25 most played artists through 2018.  I am shocked that there are no female artists.  Further, although there are female acts just outside of the top 25 (e.g. the pretenders, bonnie raitt, adele, lucinda williams, brandi carlile, joni mitchell, ingrid michaelson, sheryl crow), the top 100 is decidedly dominated by males.

| artist | 2007 | 2008 | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 |
| ------ | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| bruce springsteen | 726 | 910 | 880 | 1197 | 636 | 1536 | 765 | 1147 | 400 | 493 | 313 | 362 |
| the beatles | 366 | 591 | 635 | 685 | 768 | 792 | 634 | 1140 | 434 | 625 | 610 | 767 |
| the rolling stones | 742 | 774 | 551 | 639 | 594 | 871 | 957 | 906 | 302 | 501 | 405 | 500 |
| r. e. m. | 732 | 873 | 455 | 565 | 1006 | 812 | 731 | 652 | 282 | 294 | 254 | 277 |
| u2 | 665 | 568 | 733 | 502 | 628 | 755 | 774 | 922 | 302 | 298 | 367 | 334 |
| bob dylan | 662 | 675 | 906 | 570 | 611 | 745 | 563 | 609 | 360 | 496 | 307 | 318 |
| david bowie | 506 | 571 | 375 | 402 | 424 | 506 | 1018 | 551 | 274 | 683 | 521 | 411 |
| the black keys | 186 | 343 | 92 | 967 | 854 | 1441 | 560 | 1120 | 187 | 160 | 81 | 116 |
| wilco | 779 | 524 | 746 | 471 | 890 | 714 | 489 | 296 | 356 | 394 | 222 | 169 |
| coldplay | 268 | 817 | 651 | 310 | 906 | 833 | 556 | 912 | 250 | 300 | 106 | 126 |
| dr. dog | 46 | 487 | 151 | 1067 | 460 | 1201 | 737 | 623 | 183 | 254 | 81 | 370 |
| ryan adams | 621 | 332 | 156 | 201 | 447 | 500 | 340 | 872 | 427 | 232 | 479 | 198 |
| dave matthews band | 285 | 302 | 754 | 381 | 395 | 950 | 650 | 411 | 154 | 142 | 97 | 275 |
| beck | 458 | 567 | 267 | 229 | 318 | 369 | 461 | 752 | 325 | 256 | 310 | 324 |
| kings of leon | 357 | 391 | 825 | 590 | 595 | 228 | 641 | 375 | 110 | 222 | 134 | 81 |
| neil young | 455 | 511 | 504 | 370 | 358 | 269 | 362 | 415 | 283 | 349 | 345 | 297 |
| talking heads | 447 | 337 | 270 | 351 | 478 | 432 | 589 | 552 | 268 | 253 | 237 | 246 |
| my morning jacket | 355 | 818 | 231 | 239 | 861 | 364 | 314 | 293 | 576 | 169 | 103 | 126 |
| van morrison | 449 | 496 | 357 | 400 | 395 | 542 | 446 | 414 | 202 | 287 | 223 | 229 |
| amos lee | 224 | 538 | 185 | 251 | 852 | 270 | 751 | 369 | 147 | 404 | 137 | 283 |
| spoon | 548 | 377 | 293 | 611 | 233 | 137 | 242 | 801 | 314 | 127 | 533 | 159 |
| dawes | 0 | 0 | 87 | 495 | 945 | 442 | 952 | 233 | 379 | 300 | 209 | 324 |
| paul simon | 289 | 252 | 272 | 376 | 982 | 479 | 434 | 375 | 178 | 367 | 162 | 170 |
| elvis costello | 557 | 494 | 416 | 443 | 478 | 458 | 314 | 398 | 183 | 197 | 213 | 156 |
| death cab for cutie | 85 | 799 | 532 | 391 | 862 | 389 | 283 | 231 | 230 | 39 | 103 | 312 |
