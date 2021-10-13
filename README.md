# shortwave

Publish a private podcast feed for a directory full of audio files. This program is like a static site publisher for a podcast feed.


## Usage

To use shortwave, make a new directory on disk where you'll keep the podcast files. These will be the files you upload to a web host that supports serving static sites. Make this directory look like:

```text
example-cast/
├── episodes/
├── feed.hjson
└── podcast-artwork.jpg
```

Copy the [`feed.hjson.example`](feed.hjson.example) to `example-cast/feed.hjson` to get it started. This [Hjson][] file contains all the info about your feed & each entry in it. Fill in your feed metadata at the top level. (Make up your own silly logo for the `example-cast.jpg` artwork! It will appear as the podcast art when you play the podcasts.)

To add your first episode:

1. Add a new audio file to the `episodes/` directory.
1. In `feed.hjson`, add a new entry to the `episodes:` list describing the episode.
1. Run shortwave.py. It will write out a new `feed.xml` suitable for use in a podcast player!
1. Upload your updated podcast files to your static site host.

With the podcast uploaded, you can add the feed to your podcast player of choice!

The feed & episodes are all marked as private, so they should not appear in the iTunes directory. If your podcast player behaves differently for private podcast feeds, you should see that behavior too. ([Overcast][] disables episode sharing features, for example.)

Now whenever you want to add a new audio file to your podcast, repeat those steps!

shortwave uses [podgen][] to produce the podcast feed, so it will automatically determine the duration of episodes that are in one of [tinytag's supported media formats][tinytag-media].

[Hjson]: https://hjson.github.io
[Overcast]: https://overcast.fm
[podgen]: https://podgen.readthedocs.io/en/latest/
[tinytag-media]: https://github.com/devsnd/tinytag#features
