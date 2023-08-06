#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Blue Yonder coding task for Python Developer position.

Given a plaintext file containing URLs, one per line, e.g.:

http://mywebserver.com/images/271947.jpg
http://mywebserver.com/images/24174.jpg
http://somewebsrv.com/img/992147.jpg

Write a script that takes this plaintext file as an argument and downloads all
images, storing them on the local hard disk. Approach the problem as you would
any task in a normal day’s work. Imagine this code will be used in important
live systems, modified later on by other developers, and so on.

Please use the Python programming language for your solution. We prefer to
receive your code in GitHub or a similar repository.

.. moduleauthor: Florian Aldehoff <by_get@biohazardous.de>
"""

import sys


def sanitize_urls(file_object):
    """Basic input sanitation filtering out whitespace, empty lines, and unsafe
    characters.

    Invalid URLs, missing and wrong schemata are handled by Requests module!

    Parameters
    ----------
    file_object : file, required
        An opened file object for a text file with one line per URL.

    Yields
    ------
    Lazy iterator over sanitized URLs.
    """

    from urllib.parse import quote

    for line in file_object:
        # remove leading and trailing whitespace
        url = line.strip()
        # skip empty lines
        if len(url) == 0:
            continue
        # quote unsafe URL characters (see http://www.ietf.org/rfc/rfc3986.txt)
        url = quote(url, safe="%/:=&?~#+!$,;'@()*[]")

        yield url


def get_url(url, session=None, filter_html=True, **requests_kwargs):
    """Retrieve server response from given URL as byte stream.

    Attempts to filter out non-image responses like HTML pages by default.
    Subsequent requests to the same server will re-use a connection of the
    given session if possible.

    Parameters
    ----------
    url : str, required
        A valid URL for an image resource.
    filter_html : bool, optional
        Should HTML and other text-based responses be filtered out?
    requests_kwargs : optional
        Additional keyword arguments to be passed on to the requests module.

    Returns
    -------
    A Response object of the requests module.

    Raises
    ------
    TypeError
        Response is not an image.
    HTTPError
        Server responds with HTML status code indicating an error.
    InvalidSchema
        The URL is invalid and can not be requested.
    MissingSchema
        A valid protocol schema, eg. 'http://', is missing from the URL.
    ReadTimeout
        Server did not respond within 10 seconds.
    """
    import requests

    # use streaming to avoid downloading entire response to memory first
    if session is not None:
        response = session.get(url, stream=True, **requests_kwargs)
    else:
        response = requests.get(url, stream=True, **requests_kwargs)
    response.raise_for_status()
    # always decode compressed server responses (GZIP, deflate)
    response.raw.decode_content = True
    # filter out HTML and other text-based responses by checking for encoding
    if filter_html and response.encoding is not None:
        raise TypeError('not an image')
    return response


def hash_string(some_string):
    """Calculate the human-readable SHA256 hash of a string.

    Parameters
    ----------
    some_string : str, required
        String to be hashed.

    Returns
    -------
    String of 64 hexadecimal characters.

    """
    import hashlib
    return hashlib.sha256(some_string.encode()).hexdigest()


def main():
    """Download images from a given plaintext file of URLs.

    Good URLs and the resulting image file names are written to STDOUT. Bad
    URLs and their error codes are written to STDERR. Images are saved to the
    working directory and named with the SHA256 hash of the (clean) source URL
    to avoid overwriting homonymous files from other URLs.

    Redirects are handled transparently and non-image responses (e.g. HTML from
    domain parking servers) are filtered out. Existing connections are re-used
    where possible to reduce the overhead of connection negotiation when
    repeatedly requesting images from the same server.
    """

    import time
    import argparse
    import logging as log
    import os.path
    import shutil
    import requests
    from requests.exceptions import (ConnectionError, HTTPError, InvalidSchema,
                                     MissingSchema, ReadTimeout)

    start = time.time()

    # parse arguments
    parser = argparse.ArgumentParser(description="BY image getter")
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='be more verbose')
    parser.add_argument("file", help="text file with image URLs")
    (args, remainArgs) = parser.parse_known_args()

    # configure logging
    if args.verbose:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        log.info("Verbose output activated.")
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")

    # check for valid path to TXT file
    if not (os.path.isfile(args.file)):
        log.error("no such file: %s" % (args.file,))
        exit(1)
    elif not (args.file.endswith('.TXT') or args.file.endswith('.txt')):
        log.error("not a text file: %s" % (args.file,))
        exit(1)

    # process list of URLs
    with open(args.file, 'r') as f:
        # superficial input sanitation, malformed URLs are handled later
        urls = sanitize_urls(f)

        # sorting URLs facilitates re-use of connections
        urls = sorted(urls)
        session = requests.Session()

        for url in urls:
            # use hashes to avoid overwriting files with identical name
            filename = hash_string(url)

            try:
                response = get_url(url, session=session, timeout=10)
            except TypeError as e:
                log.error("%s\t%s" % (e, url))
                continue
            except ConnectionError as e:
                log.error("%s\t%s" % ("no connection", url))
                continue
            except ReadTimeout as e:
                log.error("%s\t%s" % ("timeout", url))
                continue
            except HTTPError as e:
                log.error("%s\t%s" % (e.response.status_code, url))
                continue
            except (InvalidSchema, MissingSchema) as e:
                log.error("%s\t%s" % ("invalid URL", url))
                continue

            # write image file to working directory
            with open(filename, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response

            # allow downstream processing of filenames and good URLs
            print("%s\t%s" % (filename, url), file=sys.stdout)

        session.close()

    log.info("elapsed time: %f seconds" % (time.time() - start,))
    exit(0)


if __name__ == "__main__":
    main()
