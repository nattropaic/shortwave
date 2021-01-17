#!/usr/bin/env python3

import argparse
import logging
import os.path
import sys
from urllib.parse import urljoin

import dateparser
import hjson
import podgen


def generate(args):
    with args.feedfile as f:
        feeddata = hjson.load(f)

    base_url = feeddata["url"]

    feed = podgen.Podcast()
    # The podgen docs say these are required.
    feed.name = feeddata["title"]
    feed.description = feeddata.get("description", feed.name)
    feed.website = base_url
    feed.explicit = False

    feed.image = urljoin(base_url, feeddata["image"])
    feed.language = feeddata.get("language", "en-US")

    # These feeds are private, so tell iTunes not to index the feed. (This
    # also tells Overcast to turn off its sharing features.)
    # https://podgen.readthedocs.io/en/latest/api.podcast.html#podgen.Podcast.withhold_from_itunes
    feed.withhold_from_itunes = True

    for episodedata in feeddata["episodes"]:
        episode_url = urljoin(base_url, episodedata["path"])
        episode_title = episodedata["title"]
        episode_file = episodedata["path"]
        # We should make sure the episode file exists, and we want to find the episode size anyway, so do that now.
        try:
            episode_size = os.path.getsize(episode_file)
        except FileNotFoundError:
            logging.error(
                f"The media file {episode_file} for episode {episode_title!r} doesn't exist. "
                "Please check your feed file."
            )
            return 1

        episode = feed.add_episode()
        episode.title = episode_title
        episode.link = episodedata.get("link")
        episode.authors = [podgen.Person(name) for name in episodedata.get("authors", {})]
        episode.publication_date = dateparser.parse(
            episodedata["published"], settings={"RETURN_AS_TIMEZONE_AWARE": True}
        )
        episode.explicit = episodedata.get("explicit", False)
        episode.image = episodedata.get("image")
        # Be extra clear the episode is private.
        episode.withhold_from_itunes = True

        episode.media = podgen.Media(episode_url, size=episode_size)
        episode.media.populate_duration_from(episode_file)

    feed.rss_file("feed.xml")


def main(argv):
    parser = argparse.ArgumentParser(description="Generate a podcast feed for some audio files.")
    parser.add_argument(
        "--feedfile",
        type=argparse.FileType("r"),
        default="./feed.hjson",
        help="Config file to generate a feed from (default: feed.hjson)",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    return generate(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
