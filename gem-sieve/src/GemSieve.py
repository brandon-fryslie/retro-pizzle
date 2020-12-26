
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

import google_it
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
parser.add_argument('-d', '--base-roms-dir', dest='base_roms_dir', action='store', required=True)
parser.add_argument('-p', '--platform', dest='platform', action='store', required=True)
parser.add_argument('--debug', dest='debug', action='store_true', default=False)

args = parser.parse_args()

if args.debug:
    print(logs.magenta("DEBUG MODE ENABLED"))
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


info_log(f"Sifting roms for {args.platform}.  Base roms directory: {args.base_roms_dir}")
google_it.query_roms(args.base_roms_dir, args.platform)
