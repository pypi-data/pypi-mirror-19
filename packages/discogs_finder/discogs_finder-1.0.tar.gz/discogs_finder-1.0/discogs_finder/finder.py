#!/usr/bin/env python

import json
import urllib2


def load_data(username):
    """ Gets user collection (in all folders) for the 
    specified user from the Discogs API.
    
    Args:
        username (string): user name
    
    Returns
        (dict): user collection
    
    Example:
    >>> load_data('tim6her') # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        [{u'instance_id': 188396596, u'date_added': ...
    """
    url = 'https://api.discogs.com/users/%s/collection/folders/0/releases'
    url = url % username
    s_data = urllib2.urlopen(url)

    return json.load(s_data)['releases']

def release_string(d_release):
    """ Produces a string describing a release
    
    Args:
        d_release (dict): dictonary containing the release data
    
    Returns:
        (string): representing the release
    
    Example:
        >>> with open('discogs_finder/tests/test.json', 'r') as f:
        ...    r = json.load(f)
        >>> release_string(r) # doctest: +NORMALIZE_WHITESPACE
        u'Keith Jarrett: Shades (3318191)'
    """
    release_id = d_release['id']
    basics = d_release.get('basic_information', None)
    if not basics:
        raise KeyError ("Your release %d doesn't contain"
                " the field 'basic_information'" % release_id)
    artists = basics.get('artists', None)
    if len(artists):
        j = artists[0]['join']
        if j == ',':
            j = '%s ' % j
        else:
            j = ' %s ' % j
        arts = j.join((a['name'] for a in artists))
    else:
        arts = None
    
    title = basics.get('title', None)
    
    return u'{arts}: {title} ({release_id})'.format(arts=arts,
                                            title=title,
                                            release_id=release_id)

def found_in_release(data, add=None, **querry):
    """ Searches recursively in all leafes of the tree
     contained in `data` for the key value pair in `querry`
    
    Note:
        The value must only be *contained* in a leaf not
        equal the leafs value, i.e., "Kei" matches "Keith".
    
    Args:
        data (dict):    the data tree
        add (list):     address pre-fix, default `None`
        querry (dict):  the key value pair to look for
    
    Returns:
        (bool): `True` if pair was found else found
        (list): If the pair was found, its address is 
                returned, i.e., the sequence of nodes
                leading to the pair.  List indices are
                returned as `unicode(i)`.
                Note: If the pair was not found there
                is still a list returned but it
                contains an *arbitrary* address.
        (string): the matched value
    
    Example:
        >>> with open('discogs_finder/tests/test.json', 'r') as f:
        ...    r = json.load(f)
        >>> found_in_release(r, name="Keith") 
        ... # doctest: +NORMALIZE_WHITESPACE
        (True, [u'basic_information', u'artists', u'0', u'name'], 
        u'Keith Jarrett')

    """
    add = [] if not add else add
    if type(data) == list:
        sub = (found_in_release(d, add + [unicode(i)], **querry) 
                        for i, d in enumerate(data))
        
    elif type(data) == dict:
        field = querry.keys()[0]
        value = querry[field]
        if unicode(value).lower() in unicode(data.get(field, '')).lower():
            return True, add + [unicode(field)], data[field]
        
        sub = (found_in_release(d, add + [k], **querry)
                        for k, d in data.iteritems())
        
    else:
        return False, add, None
    
    hits = [(f, a, v) for f, a, v in sub if f]

    if len(hits):
        return hits[0]
    else:
        return False, add, None
        
if __name__ == "__main__":
    import doctest
    doctest.NORMALIZE_WHITESPACE
    doctest.ELLIPSIS
    doctest.testmod()