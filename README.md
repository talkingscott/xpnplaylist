# XPN Playlist Acquisition and Summarization

[WXPN](http://xpn.org) is a radio station from the University of Pennsylvania in Philadelphia.  Their daily playlists are available on their web site back to 2007-01-19.  My curiosity about whether they *ever* played [Eliza Doolittle](https://www.elizalovechild.com/) led me to write the scripts here.

## Scripts

The get_playlist.py script downloads daily playlists as JSON.  It accepts partial dates, so that 2018-03-15 specifies a single day, 2018-03 specifies all days in that month, and 2018 specifies all days in that year.  The script also accepts an optional directory argument.

The script has been enhanced to alternatively download playlists from XPN2 and [The Current](https://thecurrent.org).

```bash
$ pipenv run get_playlist --help
usage: get_playlist.py [-h] [-D DIRECTORY] [-S SERVICE] date [date ...]

Get XPN Playlists

positional arguments:
  date                  The date(s) to fetch (yyyy-MM-dd or yyyy-MM or yyyy)

optional arguments:
  -h, --help            show this help message and exit
  -D DIRECTORY, --directory DIRECTORY
                        The directory for output
  -S SERVICE, --service SERVICE
                        The service (xpn|xpn2|thecurrent)

$ pipenv run get_playlist -S xpn -D playlists/xpn/2018 2018-11-29 2018-11-30 2018-12
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

$ pipenv run summarize_playlists -o counts/xpn/count-2018.json playlists/xpn/2018
```

## Results

I tabulated annual totals for some artists I like, but never seem to hear, along with a few "similar" artists that I do hear.

| artist | 2007 | 2008 | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 |
| ------ | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| bitter:sweet | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| dido | 18 | 40 | 26 | 31 | 34 | 55 | 30 | 24 | 20 | 21 | 14 | 22 | 35 | 18 | 21 |
| eliza doolittle | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| fatboy slim | 14 | 17 | 17 | 6 | 25 | 38 | 8 | 9 | 8 | 11 | 12 | 14 | 13 | 14 | 17 |
| feist | 394 | 190 | 53 | 54 | 226 | 294 | 70 | 73 | 48 | 47 | 76 | 52 | 57 | 56 | 50 |
| ingrid michaelson | 84 | 219 | 210 | 189 | 88 | 361 | 62 | 411 | 68 | 62 | 38 | 49 | 50 | 31 | 32 |
| jem | 17 | 19 | 14 | 14 | 13 | 24 | 10 | 6 | 8 | 2 | 4 | 1 | 3 | 3 | 2 |
| joss stone | 214 | 51 | 81 | 45 | 93 | 218 | 56 | 49 | 119 | 46 | 34 | 48 | 51 | 48 | 36 |
| k. t. tunstall | 219 | 93 | 36 | 163 | 108 | 104 | 141 | 58 | 54 | 59 | 45 | 153 | 68 | 51 | 45 |
| kate bush | 44 | 39 | 53 | 59 | 73 | 99 | 46 | 54 | 64 | 53 | 71 | 87 | 73 | 77 | 89 |
| lana del rey | 0 | 0 | 0 | 0 | 53 | 394 | 70 | 246 | 152 | 94 | 220 | 119 | 216 | 120 | 104 |
| lenka | 0 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| lily allen | 194 | 76 | 134 | 51 | 45 | 70 | 25 | 26 | 19 | 17 | 19 | 21 | 25 | 29 | 24 |
| material | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 3 | 0 |
| paramore | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 1 | 0 | 1 |
| regina spektor | 96 | 22 | 159 | 77 | 25 | 241 | 34 | 26 | 16 | 22 | 15 | 4 | 20 | 9 | 5 |
| sara bareilles | 8 | 80 | 19 | 25 | 33 | 36 | 14 | 14 | 11 | 12 | 9 | 44 | 159 | 36 | 29 |
| sia | 9 | 16 | 10 | 13 | 13 | 19 | 9 | 6 | 3 | 5 | 5 | 7 | 3 | 6 | 4 |
| sofi tukker | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 0 |
| the crystal method | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| thievery corporation | 29 | 94 | 112 | 31 | 27 | 32 | 25 | 44 | 21 | 25 | 25 | 16 | 21 | 15 | 10 |

I also tabulated annual totals for the 25 most played artists through 2018.  I am suprised that there are only two female artists (the pretenders and bonnie raitt).

| artist | 2007 | 2008 | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 |
| ------ | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| bruce springsteen | 378 | 473 | 461 | 614 | 327 | 1536 | 389 | 615 | 400 | 493 | 313 | 362 |
| the beatles | 202 | 298 | 326 | 353 | 394 | 792 | 332 | 626 | 434 | 625 | 610 | 767 |
| the rolling stones | 376 | 396 | 281 | 325 | 310 | 871 | 488 | 503 | 302 | 501 | 405 | 500 |
| bob dylan | 356 | 353 | 486 | 307 | 324 | 745 | 303 | 370 | 360 | 496 | 307 | 318 |
| u2 | 336 | 290 | 383 | 256 | 322 | 755 | 391 | 502 | 302 | 298 | 367 | 334 |
| r. e. m. | 381 | 450 | 236 | 293 | 525 | 812 | 376 | 356 | 282 | 294 | 254 | 277 |
| david bowie | 263 | 296 | 199 | 211 | 221 | 506 | 526 | 303 | 274 | 683 | 521 | 411 |
| the black keys | 98 | 184 | 51 | 508 | 448 | 1441 | 294 | 597 | 187 | 160 | 81 | 116 |
| wilco | 416 | 278 | 403 | 246 | 470 | 714 | 258 | 169 | 356 | 394 | 222 | 169 |
| dr. dog | 40 | 259 | 80 | 562 | 242 | 1201 | 380 | 346 | 183 | 254 | 81 | 370 |
| coldplay | 138 | 423 | 332 | 159 | 469 | 833 | 281 | 489 | 250 | 300 | 106 | 126 |
| ryan adams | 330 | 176 | 88 | 107 | 237 | 500 | 178 | 511 | 427 | 232 | 479 | 198 |
| dave matthews band | 143 | 155 | 380 | 193 | 200 | 950 | 329 | 228 | 154 | 142 | 97 | 275 |
| beck | 247 | 298 | 146 | 122 | 168 | 369 | 244 | 411 | 325 | 256 | 310 | 324 |
| neil young | 234 | 267 | 265 | 196 | 190 | 269 | 193 | 243 | 283 | 349 | 346 | 297 |
| dawes | 0 | 0 | 48 | 265 | 492 | 442 | 493 | 122 | 379 | 300 | 209 | 324 |
| van morrison | 231 | 256 | 191 | 211 | 209 | 542 | 233 | 240 | 202 | 287 | 223 | 229 |
| talking heads | 231 | 181 | 146 | 188 | 252 | 432 | 307 | 306 | 268 | 253 | 237 | 246 |
| spoon | 294 | 209 | 158 | 326 | 130 | 137 | 130 | 467 | 314 | 127 | 533 | 159 |
| my morning jacket | 182 | 422 | 128 | 128 | 452 | 364 | 164 | 161 | 576 | 169 | 103 | 126 |
| paul simon | 151 | 131 | 143 | 196 | 512 | 479 | 227 | 215 | 178 | 367 | 162 | 170 |
| the pretenders | 165 | 302 | 211 | 133 | 227 | 485 | 224 | 155 | 178 | 324 | 239 | 241 |
| amos lee | 120 | 275 | 95 | 131 | 444 | 270 | 383 | 195 | 147 | 404 | 137 | 283 |
| elvis costello | 296 | 265 | 224 | 238 | 255 | 458 | 168 | 217 | 183 | 197 | 213 | 156 |
| bonnie raitt | 167 | 178 | 128 | 134 | 144 | 878 | 223 | 150 | 131 | 446 | 141 | 135 |
