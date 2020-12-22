
# This script would ideally:
# Take a system name (SNES, NES, etc) as an argument
# Output a folder of roms containing the top rated games for that system
# e.g., "Every game rated above a 7 avg"

# First we need a place to query the data for reviews (Giantbomb API?)

# Should I try to query a list of high rated games first, then match those to roms?
# Or grab a list of roms and try to match them to reviews?

# We could manually enter a list.  We'll choose SNES.  We'll try that next.

# Maybe Interesting https://github.com/BirdAPI/GameSpot-Scraper-API

import argparse
import logging

import fetch_review
import load_cache
import logs
import match_gems
import metacritic
import nes_filter
import save_cache
from logs import info_log, error_log

# got an API key!

# Lets see if I can grab the list right from giantbomb


info_log("Beginning Gem Sieve")


parser = argparse.ArgumentParser(description='Search for Gems')
parser.add_argument('--cache-pages', dest='should_cache_pages', action='store_true', default=False)
parser.add_argument('--load', dest='load_cached_pages', action='store_true', default=False)
parser.add_argument('--fetch', dest='fetch_review', action='store_true', default=False)
parser.add_argument('--metacritic', dest='metacritic', action='store_true', default=False)
parser.add_argument('--match-gems', dest='match_gems', action='store_true', default=False)
parser.add_argument('--nes', dest='nes', action='store_true', default=False)
parser.add_argument('--debug', dest='debug', action='store_true', default=False)

args = parser.parse_args()

if args.debug:
    print(logs.magenta("DEBUG MODE ENABLED"))
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

if args.should_cache_pages:
    info_log("Caching pages")
    save_cache.cache_all_pages(initial_offset=70000)

elif args.load_cached_pages:
    info_log("Loading cached pages")
    load_cache.load_cached_pages()

elif args.fetch_review:
    info_log("Fetching ratings")
    fetch_review.fetch_review()

elif args.metacritic:
    info_log("Querying metacritic")
    metacritic.query()

elif args.match_gems:
    info_log("Matching Gems")
    gems = metacritic.query()
    match_gems.match(gems)

elif args.nes:
    info_log("NES GAMES")
    nes_filter.filter_and_delete()

else:
    error_log("No action specified")
