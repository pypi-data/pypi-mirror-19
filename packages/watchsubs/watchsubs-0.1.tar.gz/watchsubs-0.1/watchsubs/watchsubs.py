#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import time
import os
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from subliminal import download_best_subtitles
from subliminal import save_subtitles, region, scan_video
from subliminal.video import VIDEO_EXTENSIONS
from babelfish import Language

logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)


def get_extension(path):
    if os.path.isfile(path):
        basename = os.path.basename(path)
        return ("." + basename.split(".")[-1]).lower()
    return ""


class MovieHandler(FileSystemEventHandler):
    def __init__(self, langs):
        self.langs = langs

    def on_created(self, event):
        print(event.src_path)
        if not get_extension(event.src_path) in VIDEO_EXTENSIONS:
            return
        try:
            movie = scan_video(event.src_path)
            subtitles = download_best_subtitles([movie], self.langs)
            logging.info("Downloaded subtitles for movie %s" % movie.name)
            save_subtitles(movie, subtitles[movie])
        except Exception as e:
            logging.info("Exception [%s] while downloading" % str(e))


def make_observer(path, langs, recursive=True):
    # subliminal config
    region.configure(
        'dogpile.cache.dbm', arguments={'filename': '.cachefile.dbm'})
    event_handler = MovieHandler(langs)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=recursive)
    return observer


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True, type=str)
    parser.add_argument('--langs', type=str, nargs='+', default=['eng'])
    parser.add_argument('--non_recursive', action='store_true')
    args = parser.parse_args()
    path = os.path.abspath(args.path)
    langs = set([Language(l) for l in args.langs])

    # event handlers
    observer = make_observer(path, langs, recursive=not args.non_recursive)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    return
