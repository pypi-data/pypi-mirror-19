#!/usr/bin/env python3
# Ducker - search with DuckDuckGo from the command line

# Copyright (C) 2016 Jorge Maldonado Ventura

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import logging
import os
import webbrowser

from . import __version__

PROGRAM_DESCRIPTION = 'search with DuckDuckGo from the command line'

# Logging for debugging purposes
logging.basicConfig(format='[%(levelname)s] %(message)s')
logger = logging.getLogger()


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION,
                                     prog='Ducker')

    # First display -h, --help and --version
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + __version__,
                        help='output version information and exit')

    parser.add_argument('-m', '--multiple-search', action='store_true',
                        help='launch a search for every word given')

    # Search categories
    parser.add_argument('-i', '--image-search', action='store_true',
                        help='search for images')
    parser.add_argument('-v', '--video-search', action='store_true',
                        help='search for videos')
    parser.add_argument('-w', '--website-search', action='store_true',
                        help='search for websites')

    parser.add_argument('-H', '--no-javascript', action='store_true',
                        help='search with DuckDuckGo without using JavaScript')
    parser.add_argument('-l', '--lite', action='store_true',
                        help='search with DuckDuckGo lite interface.')

    # Positional arguments
    parser.add_argument('search_str', metavar='search_str',
                        nargs='+', help='what you want to search')

    return parser.parse_args()


def build_search_url(search_str, args):
    """Build the search URL with the suplied search string and arguments."""

    base_url = 'https://duckduckgo.com/'
    search_category = ''

    if args.no_javascript:
        base_url += 'html/'
    elif args.lite:
        base_url += 'lite/'
    else:
        if args.website_search:
            search_category = '&ia=web'
        elif args.image_search:
            search_category = '&ia=images'
        elif args.video_search:
            search_category = '&ia=videos'

    logger.debug('Built %s search for %s', search_str, search_category[4:])

    return '{}?q={}{}'.format(base_url, search_str, search_category)


def open_url(url):
    """Open an URL in the user's default web browser.
    Whether the browser's output (both stdout and stderr) are suppressed
    depends on the boolean attribute ``open_url.suppress_browser_output``.
    If the attribute is not set upon a call, set it to a default value,
    which means False if BROWSER is set to a known text-based browser --
    elinks, links, lynx or w3m; or True otherwise.
    """
    if not hasattr(open_url, 'suppress_browser_output'):
        open_url.suppress_browser_output = (os.getenv('BROWSER') not in
                                            ['elinks', 'links', 'lynx', 'w3m'])
    logger.debug('Opening %s', url)
    if open_url.suppress_browser_output:
        _stderr = os.dup(2)
        os.close(2)
        _stdout = os.dup(1)
        os.close(1)
        fd = os.open(os.devnull, os.O_RDWR)
        os.dup2(fd, 2)
        os.dup2(fd, 1)
    try:
        webbrowser.open(url)
    finally:
        if open_url.suppress_browser_output:
            os.close(fd)
            os.dup2(_stderr, 2)
            os.dup2(_stdout, 1)


def make_searchs():
    """Make the searchs specified by the user."""
    args = parse_args()

    if args.multiple_search:
        for search_str in args.search_str:
            search_url = build_search_url(search_str, args)
            open_url(search_url)
    else:
        search_url = build_search_url(' '.join(args.search_str), args)
        open_url(search_url)
