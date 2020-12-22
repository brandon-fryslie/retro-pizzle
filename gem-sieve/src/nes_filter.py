import os
import re
import shutil
from pprint import pprint
from typing import List, Dict

import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import process

from logs import info_log, error_log

BASE_ROMS_DIR = "/Volumes/roms"

def clean_rom_name(entry: str) -> str:
    filename, extension = os.path.splitext(entry)
    cleaned = re.sub('\(.+\)', '', filename).strip()
    return cleaned

def query_nes_roms() -> List[os.DirEntry]:
    nes_roms_dir = f"{BASE_ROMS_DIR}/nes"
    entries: List[os.DirEntry]

    rom_data = []
    with os.scandir(nes_roms_dir) as entries:
        for entry in entries:
            if entry.is_file():
                rom_data.append(entry)

    return rom_data

def extract_game_data(el: BeautifulSoup) -> Dict[str, str]:
    game_data = {}

    # These are the cells in the table
    cells = el.find_all('td')

    if len(cells) != 4:
        error_msg = "ERROR: Cells did not have expected number of elements (4)"
        error_log(error_msg)
        pprint(cells)
        raise RuntimeError(error_msg)

    title = cells[0].find('a').text
    publisher = cells[1].text
    year = cells[2].text
    grade = cells[3].text

    # info_log(f"Extracted game data: '{title}' '{publisher}' '{year}' '{grade}'")

    game_data['title'] = title
    game_data['publisher'] = publisher
    game_data['year'] = year
    game_data['grade'] = grade

    return game_data

def print_game_info(game_data):
    info_log(f"=== Game: {game_data['title']} [Metascore: {game_data['metascore']}] (User Score: {game_data['userscore']}) ===")

# Only works w/ newer platforms :/
def query_nes_scores() -> List[Dict[str, str]]:
    base_url = "https://videogamecritic.com"
    url_path = f"nes.htm"

    url = f"{base_url}/{url_path}"

    headers = {
        'User-Agent': 'Chuck Norris',
    }

    # get data
    r = requests.get(url, headers = headers)

    # parsing html
    soup = BeautifulSoup(r.content, features='lxml')

    # info_log(f"Got request.  Content len: {len(r.content)}")

    # the HTML elements for each game on the list
    game_blocks = soup.select('#myTable tbody tr')

    return [extract_game_data(el) for el in game_blocks]

def filter_nes_scores(all_data):
    """
    Filter the scores by some criteria (like which games are fun)
    :return:
    """
    info_log("Filtering data")

    return all_data

def query(min_metascore: int = 70, min_userscore: float = 7.0):
    all_data = query_nes_scores()

    gems = []
    # filter the data
    for game in all_data:
        if game['metascore'] > min_metascore or game['userscore'] > min_userscore:
            # info_log(f"Found a Gem! {game['title']}")
            gems.append(game)

    # print("Found Gems:")
    # for gem in gems:
    #     print_game_info(gem)

    return gems

def get_score_for_rom(entry, score_data):
    def _processor(item):
        if type(item) == str:
            return item

        return item['title']

    clean_name = clean_rom_name(entry.name)
    result, fuzz_score = process.extractOne(clean_name, choices=score_data, processor=_processor)

    if fuzz_score < 90:
        # info_log(f"Fuzz score below threshold.  Could not find review for: '{clean_name}'.  Fuzz found: '{result['title']}'. Fuzz score: {fuzz_score}")
        return {'score': None, 'clean_name': clean_name, 'entry': entry}

    return {'score': result, 'clean_name': clean_name, 'entry': entry}

def filter_and_delete():
    """
    Query good games, delete bad ones
    :return:
    """
    score_data = query_nes_scores()
    info_log("Queried NES data")

    all_rom_data = query_nes_roms()

    rom_scores = [get_score_for_rom(rom_entry, score_data) for rom_entry in all_rom_data]

    unreviewed_path = f"{BASE_ROMS_DIR}/nes-unreviewed"
    os.makedirs(unreviewed_path, exist_ok=True)

    lowscore_path = f"{BASE_ROMS_DIR}/nes-lowscore"
    os.makedirs(lowscore_path, exist_ok=True)

    for rom_score in rom_scores:
        if rom_score['score'] is None:
            # Move roms to unreviewed folder
            orig_path = rom_score['entry'].path
            dest_path = f"{unreviewed_path}/{rom_score['entry'].name}"
            info_log(f"Moving unreviewed game from '{orig_path}' to '{dest_path}'")
            shutil.move(orig_path, dest_path)

        if rom_score['score'] is not None:
            letter_grade = rom_score['score']['grade']
            if re.search(r"A|B", letter_grade):
                info_log(f"Found good review match: Letter grade: {letter_grade} {rom_score['clean_name']}.  Leaving in place")
            else:
                orig_path = rom_score['entry'].path
                dest_path = f"{lowscore_path}/{rom_score['entry'].name}"
                info_log(f"Found bad review: Letter grade: {letter_grade}.  Moving from '{orig_path}' to '{dest_path}'")
                shutil.move(orig_path, dest_path)


    # for rom_entry in all_rom_data:
    #     rom_score = get_score_for_rom(rom_entry, score_data)

        # info_log(f"Rom entry {rom_entry.path} has score {rom_score['grade']} ({rom_score['title']})")

    # compare rom data to score data

    # pprint(all_data)
