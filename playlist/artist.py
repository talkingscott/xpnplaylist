"""
Functions for artists
"""

def canonical_name(artist):
    """ Normalize names across variations """
    name = artist.lower()
    if name == 'rem' or name == 'r.e.m.':
        name = 'r. e. m.'
    elif name == 'kt tunstall' or name == 'k.t. tunstall':
        name = 'k. t. tunstall'
    return name
