"""
Functions for artists
"""
import re

def canonical_name(artist):
    """ Normalize names across variations """
    name = re.sub(r' {2,}', ' ', artist.lower())
    if name[:2] == '((':
        name = name[2:]
    if name in ('rem', 'r.e.m.'):
        name = 'r. e. m.'
    elif name in ('kt tunstall', 'k t tunstall', 'k.t. tunstall'):
        name = 'k. t. tunstall'
    elif name in ('kd lang', 'k d lang', 'k.d. lang'):
        name = 'k. d. lang'
    elif name in ('st vincent', ):
        name = 'st. vincent'
    return name
