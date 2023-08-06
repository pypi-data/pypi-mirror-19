#!python
#
# This file is part of https://github.com/zsquareplusc/python-embedded-launcher
# (C) 2016 Chris Liechti <cliechti@gmx.net>
#
# SPDX-License-Identifier:    BSD-3-Clause
"""
Extract the official Python embedded distribution

- download when necessary
- extract a cached version by default
- 32/64 bit selection
- custom URL, force download
"""
import argparse
import platform
import os
import re
import sys
import zipfile
import requests

DEFAULT_VERSION = '3.6.0'
URL_TEMPLATE = 'https://www.python.org/ftp/python/{version}/python-{version}-embed-{bits}.zip'


def get_url(version, bits):
    return URL_TEMPLATE.format(version=version, bits='amd64' if bits == 64 else 'win32')


def extract(url, destination, force_download=False):
    """\
    extract zip file from cache, download if needed.
    e.g. extract(URL_32, 'python3-minimal')
    """
    # where to store
    cache_dir = os.path.abspath(os.path.expandvars('%LOCALAPPDATA%/python-embedded-launcher/cache'))  # XXX windows only
    cache_name = os.path.join(cache_dir, re.sub(r'[^\w]', '', url))
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    # download
    if not os.path.exists(cache_name) or force_download:
        sys.stderr.write('downloading {} to {}\n'.format(url, cache_name))
        response = requests.get(url, stream=True)
        with open(cache_name, 'wb') as downloaded_data:
            for chunk in response.iter_content(2**20):
                downloaded_data.write(chunk)
    else:
        sys.stderr.write('using cached file {}\n'.format(cache_name))

    if not os.path.exists(cache_name):
        sys.stderr.write('failed to download/load from cache: file not found: {}\n'.format(cache_name))
        raise IOError('file not found: {!r}'.format(cache_name))

    sys.stderr.write('extracting to {}\n'.format(destination))
    with zipfile.ZipFile(cache_name) as archive:
        archive.extractall(destination)


def main():
    """Console application entry point"""
    parser = argparse.ArgumentParser(description='download/extract for python3-minimal')

    group_out = parser.add_argument_group('output options')
    group_out.add_argument('-d', '--directory', metavar='DIR', default='.',
                           help='set a destination directory, a subdirectory NAME will be creted [default: %(default)s]')
    group_out.add_argument('-n', '--name', metavar='NAME', default='python3-minimal',
                           help='set a directory name [default: %(default)s]')

    group_download = parser.add_argument_group('download options')
    group_bits = group_download.add_mutually_exclusive_group()
    group_bits.add_argument('--32', dest='bits32', action='store_true', default=False,
                           help='force download of 32 bit version')
    group_bits.add_argument('--64', dest='bits64', action='store_true', default=False,
                           help='force download of 64 bit version')
    group_download.add_argument('--this-version', action='store_true', default=False,
                           help='choose this Python version that is running now')
    group_download.add_argument('-p', '--python-version', default=DEFAULT_VERSION, help='choose Python version (major.minor, default=%(default)s)')
    group_download.add_argument('--url', help='override download URL')
    group_download.add_argument('-f', '--force-download', action='store_true', default=False,
                                help='force download (ignore/overwrite cached file)')

    args = parser.parse_args()

    #~ print args

    if args.bits32:
        bits = 32
    elif args.bits64:
        bits = 64
    elif platform.architecture()[0] == '64bit':  # autodetect
        bits = 64
    else:
        bits = 32

    if args.this_version:
        args.python_version = '{0.major}.{0.minor}.{0.micro}'.format(sys.version_info)

    if args.url is None:
        args.url = get_url(args.python_version, bits)

    python_destination = os.path.join(args.directory, args.name)
    extract(args.url, python_destination, args.force_download)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    main()
