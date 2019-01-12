import json
import os.path
import sys

years = list(range(2007, 2019))

artist_counts = {}
artists = set()
with open('artists.txt') as fp:
    for line in fp:
        artist = line.strip().lower()
        artist_counts[artist] = [0] * len(years)
        artists.add(artist)

for i, year in enumerate(years):
    filename = os.path.join('playlist-counts', f'count-{str(year)}.json')
    with open(filename) as fp:
        counts = json.load(fp)
        for ac in counts:
            if ac['artist'].lower() in artists:
                artist_counts[ac['artist'].lower()][i] = ac['count']

print('artist\t' + '\t'.join(map(str, years)))
for artist, counts in artist_counts.items():
    print(artist + '\t' + '\t'.join(map(str, counts)))

print('| artist | ' + ' | '.join(map(str, years)) + ' |', file=sys.stderr)
print('| ------ | ' + ' | '.join(map(lambda y: '----', years)) + ' |', file=sys.stderr)
for artist, counts in artist_counts.items():
    print('| ' + artist + ' | ' + ' | '.join(map(str, counts)) + ' |', file=sys.stderr)
