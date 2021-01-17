#!/usr/bin/env python3

import argparse
import sys
from urllib.parse import urljoin

from feedgen.feed import FeedGenerator
import hjson


def generate(args):
    with args.feedfile as f:
        feeddata = hjson.load(f)

    feed = FeedGenerator()
    feed.load_extension("podcast")

    base_url = feeddata["url"]

    feed.id(base_url)
    feed.title(feeddata["title"])
    feed.language(feeddata.get("language", "en"))
    feed.author(name=feeddata["author"])
    feed.link(href=base_url, rel="alternate")
    feed.logo(urljoin(base_url, feeddata["logo"]))

    # These feeds are private.
    feed.podcast.itunes_block(True)

    for episodedata in feeddata["episodes"]:
        episode_url = urljoin(base_url, episodedata["path"])

        episode = feed.add_entry()
        episode.id(episode_url)
        episode.title(episodedata["title"])
        episode.description(episodedata["description"])
        episode.link(href=episodedata["link"])
        episode.enclosure(episode_url)

    feed.atom_file("atom.xml", pretty=True)


def main(argv):
    parser = argparse.ArgumentParser(description="Generate a podcast feed for some audio files.")
    parser.add_argument(
        "--feedfile",
        type=argparse.FileType("r"),
        default="./feed.hjson",
        help="Config file to generate a feed from (default: feed.hjson)",
    )
    args = parser.parse_args(argv)

    generate(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
