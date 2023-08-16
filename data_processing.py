import pandas as pd

def cleanse_twitch_data(twitch_data: pd.DataFrame) -> pd.DataFrame:
    game_names_to_filter = ['Counter-Strike: Global Offensive', 'Terraria',
                            'Grand Theft Auto V', 'Dota 2',
                            "PLAYERUNKNOWN'S BATTLEGROUNDS", 'Rust',
                            'Stardew Valley', 'Rocket League',
                            'Cyberpunk 2077', 'Apex Legends']

    twitch_data = twitch_data[(twitch_data['Year'] >= 2017) & (twitch_data['Year'] <= 2021)]
    # twitch_data['Year-Month'] = twitch_data['Year'].astype(str) + "-" + twitch_data['Month'].astype(str)
    twitch_data = twitch_data[twitch_data['Game'].isin(game_names_to_filter)]
    twitch_data = twitch_data[['Game', 'Month', 'Year', # 'Year-Month',
                                'Peak_viewers', 'Avg_viewers', 'Hours_watched']]
    return twitch_data
    
def cleanse_player_data(player_data: pd.DataFrame) -> pd.DataFrame:
    game_names_to_filter = ['Counter-Strike: Global Offensive', 'Terraria',
                            'Grand Theft Auto V', 'Dota 2',
                            "PLAYERUNKNOWN'S BATTLEGROUNDS", 'Rust',
                            'Stardew Valley', 'Rocket League',
                            'Cyberpunk 2077', 'Apex Legends']
    player_data['Game_Name'] = player_data['Game_Name'].str.replace(
           'Counter Strike: Global Offensive',
           'Counter-Strike: Global Offensive')
    player_data['Game_Name'] = player_data['Game_Name'].str.replace(
        'PUBG: Battlegrounds', "PLAYERUNKNOWN'S BATTLEGROUNDS")

    player_data[['month', 'year']] = player_data['Month_Year'].str.split(' ', expand=True)
    player_data['year'] = pd.to_numeric(player_data['year'])
    player_data = player_data[(player_data['year'] >= 2017) & (player_data['year'] <= 2021)]
    month_mapping = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
                     'May': 5, 'June': 6, 'July': 7, 'August': 8,
                     'September': 9, 'October': 10, 'November': 11,
                     'December': 12}

    player_data['month'] = player_data['month'].map(month_mapping)
    # player_data['year-month'] = player_data['year'].astype(str) + "-" + player_data['month'].astype(str)

    player_data = player_data[player_data['Game_Name'].isin(game_names_to_filter)]
    player_data = player_data[['Game_Name', 'month', 'year', # 'year-month',
                                'Gain', 'Avg_players', 'Peak_Players']]
    player_data['Gain_Rate'] = player_data['Gain'].fillna(0) / player_data['Avg_players']

    return player_data

    
def merge_data(twitch_data: pd.DataFrame,
                player_data: pd.DataFrame) -> pd.DataFrame:
    columns_1 = ['Game_Name', 'month', 'year']
    columns_2 = ['Game', 'Month', 'Year']

    merged = player_data.merge(twitch_data,
                               left_on=columns_1, right_on=columns_2,)
    merged.drop(columns=['Gain', 'Avg_players', 'Gain_Rate', 'Peak_Players', 
                         'Peak_viewers', 'Avg_viewers', 'Hours_watched',
                         'Game', 'Month', 'Year'], inplace=True)

    return merged