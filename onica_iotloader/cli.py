"""
onica-iotloader

Usage:
  onica-iotloader [--concurrency=<n>] <channel> <template> <count>
  onica-iotloader -h | --help
  onica-iotloader --version

Options:
  -h --help                         Show this screen.
  --concurrency=<n>                 Number of concurrent transfers [default: 10].
  --version                         Show version.

Examples:
  onica-iotloader mychannel template.py 10000
"""

from __future__ import print_function
from docopt import docopt
from . import __version__ as VERSION
from .loader import Loader


class App(object):
    """The app main class"""

    def __init__(self, channel, template, count, concurrency):
        self.channel = channel
        self.template = template
        self.count = count
        self.concurrency = concurrency

    def run(self):
        print("Channel: %s, Template: %s, Count: %d, Concurrency: %d" % (self.channel, self.template, self.count, self.concurrency))
        Loader(self.channel, self.template, self.count, self.concurrency).run()


def main():
    """Main CLI entrypoint."""
    options = docopt(__doc__, version=VERSION)
    app = App(options['<channel>'], options['<template>'], int(options['<count>']), int(options['--concurrency']))

    app.run()