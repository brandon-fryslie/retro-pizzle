from pprint import pprint

import requests
from bs4 import BeautifulSoup

from logs import info_log

def extract_game_data_metacritic(el):
    game_data = {}

    title_q = el.select_one(".title h3")
    if title_q is None:
        raise RuntimeError("Could not find elements")

    game_data['title'] = title_q.text


    metascore_q = el.select(".metascore_w")

    metascore = int(metascore_q[0].text)
    userscore = float(metascore_q[2].text)

    # print_game_info(game_data)

    game_data['metascore'] = metascore
    game_data['userscore'] = userscore

    return game_data

def print_game_info(game_data):
    info_log(f"=== Game: {game_data['title']} [Metascore: {game_data['metascore']}] (User Score: {game_data['userscore']}) ===")

# Only works w/ newer platforms :/
def query_scores_by_system_metacritic(platform):
    base_url = "https://www.metacritic.com"
    url_path = f"browse/games/score/metascore/all/{platform}"

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
    game_blocks = soup.find_all('td', class_='clamp-summary-wrap')

    return [extract_game_data_metacritic(el) for el in game_blocks]


def query(min_metascore: int = 70, min_userscore: float = 7.0):
    all_data = query_scores_by_system_metacritic('n64')

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
