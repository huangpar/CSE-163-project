import pandas as pd

steam_store_games = "cse-163-project-data/steam.csv"
twitch = 'cse-163-project-data/Twitch_game_data.csv'
player_data = 'cse-163-project-data/Valve_Player_Data.csv'

game_data = pd.read_csv(steam_store_games)
twitch_data = pd.read_csv(twitch)
player = pd.read_csv(player_data)


def merged_data(game_data: pd.DataFrame, twitch_data: pd.DataFrame,
                player=pd.DataFrame) -> pd.DataFrame:
    game_data['name'] = game_data['name'].str.rstrip('®')
    player['Game_Name'] = player['Game_Name'].str.replace(
           'Counter Strike: Global Offensive',
           'Counter-Strike: Global Offensive')
    player['Game_Name'] = player['Game_Name'].str.replace(
        'PUBG: Battlegrounds', "PLAYERUNKNOWN'S BATTLEGROUNDS")

    game_names_to_filter = ['Counter-Strike: Global Offensive', 'Terraria',
                            'Grand Theft Auto V', 'Dota 2',
                            "PLAYERUNKNOWN'S BATTLEGROUNDS", 'Rust',
                            'Stardew Valley', 'Rocket League',
                            'Cyberpunk 2077', 'Apex Legends']

    game_columns = game_data[['name', 'developer', 'publisher']]
    games_filtered = game_columns[game_columns['name'].isin(
        game_names_to_filter)]

    years = twitch_data[(twitch_data['Year'] >= 2017) &
                        (twitch_data['Year'] <= 2021)]
    years_filtered = years[years['Game'].isin(game_names_to_filter)]
    twitch_data_filtered = years_filtered[['Game', 'Month', 'Year',
                                           'Peak_viewers', 'Avg_viewers',
                                           'Hours_watched']]

    player[['month', 'year']] = player['Month_Year'].str.split(' ',
                                                               expand=True)
    player['year'] = pd.to_numeric(player['year'])

    month_mapping = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
                     'May': 5, 'June': 6, 'July': 7, 'August': 8,
                     'September': 9, 'October': 10, 'November': 11,
                     'December': 12}

    player['month'] = player['month'].map(month_mapping)
    player_years = player[player['year'] >= 2017]
    player_years_filtered = player_years[player_years
                                         ['Game_Name'].isin(
                                            game_names_to_filter)]
    player_data_filtered = player_years_filtered[['Game_Name', 'month', 'year',
                                                  'Percent_Gain',
                                                  'Avg_players',
                                                  'Peak_Players']]

    merged_games = games_filtered.merge(player_data_filtered, left_on='name',
                                        right_on='Game_Name', how='right')

    columns_1 = ['Game_Name', 'month', 'year']
    columns_2 = ['Game', 'Month', 'Year']

    merged = merged_games.merge(twitch_data_filtered, left_on=columns_1,
                                right_on=columns_2, how='outer')
    merged.drop(columns=['name', 'Game_Name', 'month', 'year'], inplace=True)

    return merged
