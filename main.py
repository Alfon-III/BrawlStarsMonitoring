import brawlstats
import pandas as pd
import os

from brawl_stars_parser import BrawlStarsParser 
from bs_db_manager import DBManager
from config import brawl_stars_api_key as BS_API_KEY
from config import monitorized_users

# Create Folders
current_directory = os.path.dirname(os.path.abspath(__file__))
results_folder = os.path.join(current_directory, 'results')
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

n_battles = 0

client = brawlstats.Client(BS_API_KEY)
bs_parser = BrawlStarsParser()

for gametag, user_name in monitorized_users.items():

    player = client.get_profile(gametag)
    bs_parser.set_gametag(gametag)

    battle_logs = player.get_battle_logs()

    parsed_battles = bs_parser.parse_battles_data(battle_logs.raw_data)
    parsed_profile = bs_parser.parse_profile_data(player.raw_data)

    db_manager = DBManager()
    n_battles += db_manager.add_battle_db(parsed_battles, player.tag)
    db_manager.add_user_db(parsed_profile)

    print(f"Updated user: {user_name}")

if n_battles > 0:
    print(f'New Registers Added: {n_battles}')

manager = DBManager()
manager.to_date_df()