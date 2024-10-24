"""
Request for API queries
"""

from typing import TypedDict

from datetime import datetime, timedelta
from xmlrpc.client import DateTime
# import pandas as pd

class BattleResultDict(TypedDict):
    time: str
    gametag: str
    player: str
    trophies: int
    brawler_id: int
    brawler_name: str
    gamemode: str
    duration_secs: int
    result: str

class UserDataDict(TypedDict):
    gametag: str
    username: str
    totalTrophies: int
    expLevel: int
    numBrawlers: int

class BrawlStarsParser:

    def __init__(self):
      self.gametag = ""

    def set_gametag(self, gametag):
        self.gametag = gametag

    def parse_battles_data(self, battles: list):
        
        user_times = []
        for battle_data in battles:
            
            
            if battle_data['event']['mode'] == 'duels':
                continue

            user_times.append(
                self.parse_battle_data(
                    battle=battle_data['battle'],
                    time=datetime.strptime(battle_data['battleTime'], '%Y%m%dT%H%M%S.%fZ')
                )
            )


        return user_times

    def parse_battle_data(self, battle: dict, time: DateTime) -> dict:
        """_summary_

        Args:
            battle (dict): _description_

        Returns:
            dict: _description_
        """
        
        # Find Player in Teams

        player_data = {}

        if 'players' in battle:
            for player in battle['players']:
                if player['tag'] == f'#{self.gametag}':
                    player_data = player

        if 'teams' in battle:
            for team in  battle['teams']:
                for player in team:
                    if player['tag'] == f'#{self.gametag}':
                        player_data = player


        battle_duration = 0
        battle_result = ''

        if 'result' in battle:
            battle_result = battle['result']
            battle_duration = battle['duration']
        if 'rank' in battle:
            battle_result = str(battle['rank'])
            #battle_duration = 0

        results: BattleResultDict = {
            'time': (time + timedelta(hours=2)).isoformat(),
            'gametag': self.gametag,
            'player': player_data['name'],
            'trophies': player_data['brawler']['trophies'],
            'brawler_id': player_data['brawler']['id'],
            'brawler_name': player_data['brawler']['name'],
            'gamemode': battle['mode'],
            'duration_secs': battle_duration,
            'result': battle_result,
        }
        
        return results

    def parse_profile_data(self, profile: dict) -> dict:
        """Profile data parser from api response to dict

        Args:
            profile (dict): _description_

        Returns:
            dict: _description_
        """

        profile_data: UserDataDict = {
            'gametag': self.gametag,
            'username': profile['name'],
            'totalTrophies': profile['trophies'],
            'expLevel': profile['expLevel'],
            'numBrawlers': len(profile['brawlers'])
        }

        return profile_data


