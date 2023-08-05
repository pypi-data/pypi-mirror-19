import sys
import functools

def normalize_url(url):
    """ ensure a url is "properly" constructed

    Remove trailing slashes
    Add http if http or https is not specified

    Parameters
    ----------
    url:  string
          A string to return as a url

    """
    if url.endswith('/'):
        url = url[:-1]
    if not url.startswith('http://') and not url.startswith('https://'):
        url = "http://{}".format(url)
    return url

