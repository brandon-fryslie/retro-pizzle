import os
import pathlib
import re
import shutil
from collections import defaultdict
from pprint import pprint
from typing import Dict, List

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from logs import info_log, error_log

from wcmatch import pathlib

def clean_rom_name(name: str):
    """
    Remove extra stuff and standardize the rom name for matching

    :param name:
    :return:
    """
    # remove group name, remove country name, etc
    # info_log(f"Cleaning name {name}")
    cleaned = re.sub(r"(?:-\w+)*$", '', name)

    # remove country...skip cruising usa
    if not re.match(r".*Cruis.*USA.*", cleaned):
        cleaned = re.sub("(?:_(?:USA|PAL|JAP|CRACK|PROPER_DUMP|SRAM|EEPROM|TRAINER|\+\d|Fix|Selector|NTSC2PAL|FULL|Multi6|N64))+$", '', cleaned, flags=re.IGNORECASE)

    return cleaned


def select_matches(matches: List[Dict]) -> List[Dict]:
    # Pick the best matches from the list.  still gotta return multiple in case we can't decide
    if len(matches) == 0 or len(matches) == 1:
        return matches

    def _reject(item):
        filename = item['fs_path']
        return not re.match(".*(?:_(?:JAP|PROPER_DUMP|SRAM|EEPROM|TRAINER|\+\d|Selector))+.*", filename)

    def _check_usa(item):
        filename = item['fs_path']
        return re.search("_USA", filename)

    current_matches = matches

    usa_roms = list(filter(_check_usa, current_matches))
    # Check to see if we've got a good USA match
    if len(usa_roms) > 0:
        current_matches = usa_roms

    current_matches = list(filter(_reject, current_matches))

    if len(current_matches) == 0:
        info_log("!!! WARNING !!! Couldn't decide what the best match is!  Returning all candidate roms")
        current_matches = matches

    return current_matches

# def copy_match(gem_rom_path, rom):
#     info_log(f"Found candidate {rom['fs_name']} {rom['fs_path']}")
#     info_log("Copying rom into new folder...")
#     os.makedirs(gem_rom_path, exist_ok=True)
#     dest_path = f"{gem_rom_path}/{rom['fs_name']}"
#     shutil.copytree(rom['fs_path'], dest_path)
#     info_log("Done copying")

def extract_match(gem_rom_path, rom_data):
    # find zip file, extract zip file, rename file
    from pathlib import Path
    game_name = rom_data['clean_name']
    print(f"Extracting zip file for rom {rom_data['clean_name']}")
    zip_files = list(Path(rom_data["fs_path"]).glob('*.zip'))

    if len(zip_files) == 0:
        error_log(f"Could not find zip files for game {game_name} {rom_data['fs_path']}")

    os.makedirs("/tmp/rom-tmp", exist_ok=True)
    tmp_path = f"/tmp/rom-tmp/{rom_data['fs_name']}"

    if not os.path.exists(tmp_path):
        info_log(f"Found {len(zip_files)}.  Extracting them now to {rom_data['fs_name']}")
        for zip_file in zip_files:
            os.system(f"unzip -d '{tmp_path}' '{zip_file}'")

        for zip_file in zip_files:
            print(f"- {zip_file}")
        # info_log("Extracted zip.  Finding roms")
    else:
        # info_log("Zip already extracted.  Finding roms")
        pass

    rom_extensions = ['*.rom', '*.v64', '*.z64']

    found_roms = list(pathlib.Path(tmp_path).glob(rom_extensions, flags=pathlib.glob.IGNORECASE))

    if len(found_roms) == 0:
        special_entry = None

        # find any files matching V64xxxx and rename to the proper name.  LAME
        with os.scandir(tmp_path) as entries:
            for entry in entries:
                if re.search(r"^v64.*", entry.name, flags=re.IGNORECASE):
                    special_entry = f"{tmp_path}/{entry.name}"

        if special_entry is None:
            error_log(f"ERROR: Couldn't find any roms for {rom_data['clean_name']} (path: {tmp_path})")
        else:
            found_roms = [special_entry]

    info_log(f"Found {len(found_roms)} roms to rename")
    for rom_path in found_roms:
        # todo, get extension

        info_log(f"- {rom_path} (Renaming to {rom_data['fs_name']})")
        filename, extension = os.path.splitext(rom_path)

        # rename and copy to folder
        os.system(f"mv '{rom_path}' '{gem_rom_path}/{rom_data['fs_name']}{extension.lower()}'")


def match(gems: list):
    base_rom_path = "/Volumes/Chunky1/Emulation/N64"
    all_rom_path = f"{base_rom_path}/AllRoms/n64-scene-archive"
    gem_rom_path = f"{base_rom_path}/GemRoms"

    game_names: Dict[str, List[Dict]] = defaultdict(lambda: [])

    with os.scandir(all_rom_path) as entries:
        for entry in entries:
            # print all entries that are files

            clean_name = clean_rom_name(entry.name)
            fs_name = entry.name

            game_names[clean_name].append({
                'clean_name': clean_name,
                'fs_name': fs_name,
                'fs_path': f"{all_rom_path}/{fs_name}",
            })

    clean_names = [clean_name for clean_name, game in game_names.items()]

    # only do the first 10 gems for now
    # gems = gems[:10]

    # loop thru Gems and match to game names
    for gem in gems:
        result, score = process.extractOne(gem['title'], clean_names)

        matched_games = game_names[result]

        filtered_matches = select_matches(matched_games)

        for rom in filtered_matches:
            extract_match(gem_rom_path, rom)


