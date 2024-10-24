import os

import pandas as pd
from tinydb import TinyDB, Query


class DBManager:

    def __init__(self):

        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.results_folder = os.path.join(self.current_directory, 'results')
        if not os.path.exists(self.results_folder):
            os.makedirs(self.results_folder)

        self.db_file_path = os.path.join(self.results_folder, 'bs_db.json')
        self.db = TinyDB(self.db_file_path)

    def add_battle_db(self, battle_data: list, gametag:  str):
        battle_table = self.db.table('battles')
        BattleQuery = Query()
        num_battles = 0

        for battle in battle_data:

            if not battle_table.contains(
                (BattleQuery.gametag == battle['gametag']) &
                (BattleQuery.time == battle['time'])
            ):
                battle_table.insert(battle)
                num_battles += 1
        
        return num_battles
    
    def add_user_db(self, user_data):
        user_table = self.db.table('user')
        UserQuery = Query()

        if not user_table.contains(
            (UserQuery.gametag == user_data['gametag'])
        ):
            user_table.insert(user_data)

    def to_date_df(self, gametag=''):
        battle_table = self.db.table('battles')
        
        User = Query()
        query = battle_table.search(User.gametag == gametag)

        records = battle_table.all()
        if query:
            records = query

        df = pd.DataFrame(records)
        df['time'] = pd.to_datetime(df['time'])
        df['date'] = df['time'].dt.date
        player_daily_counts  = df.groupby(['player', 'date']).size().reset_index(name='battle_count')

        print(player_daily_counts )
 
    def delete_duplicates(self):
        battle_table = self.db.table('battles')
        records = battle_table.all()
        
        # Dictionary to track unique records
        seen = {}
        duplicates = []

        for record in records:
            record_tuple = tuple(record.items())  # Create a tuple of all items in the record
            
            if record_tuple in seen:
                duplicates.append(record.doc_id)  # Store doc_id for duplicates
            else:
                seen[record_tuple] = record.doc_id  # Store doc_id for unique record

        # Remove duplicates
        for doc_id in duplicates:
            battle_table.remove(doc_ids=[doc_id])

        print(f"Removed {len(duplicates)} duplicates.")
        
    # Queries -  JSON

    def get_games_day(self, date):

        battle_table = self.db.table('battles')
        
        Battle = Query()
        query = battle_table.search(Battle.time == date)

        records = battle_table.all()
        if query:
            records = query

        df = pd.DataFrame(records)
        df['time'] = pd.to_datetime(df['time'])
        df['date'] = df['time'].dt.date
        player_daily_counts  = df.groupby(['player', 'date']).size().reset_index(name='battle_count')

        print(player_daily_counts )


# manager = DBManager()
# db = manager.db.table('user')
# print(db.all())