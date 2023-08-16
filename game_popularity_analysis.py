import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from data_processing import cleanse_twitch_data, cleanse_player_data, merge_data

def main():
    twitch_file = '/Users/ethanzwang/Desktop/Cse_163_Project/Twitch_game_data.csv'
    player_file = '/Users/ethanzwang/Desktop/Cse_163_Project/Valve_Player_Data.csv'
    developer_file = '/Users/ethanzwang/Desktop/Cse_163_Project/Game_Developer_Data.csv'

    twitch_data = pd.read_csv(twitch_file, encoding="cp1252")
    player_data = pd.read_csv(player_file, encoding="cp1252")
    developer_data = pd.read_csv(developer_file, encoding="cp1252")

    # Load and preprocess all 3 datasets, Popularity dataset, Streaming dataset, developer dataset(pre-made)
    twitch_data_clean = cleanse_twitch_data(twitch_data)
    player_data_clean = cleanse_player_data(player_data)
    
    # Calculate popularity score(popularity dataset), numpy.log((peak - avg) * gain rate / 100 + avg)
    # Popularity score answers Research qs 1
    player_data_clean['Popularity_Score'] = np.log((player_data_clean['Peak_Players'] - player_data_clean['Avg_players']) *
                                                      player_data_clean['Gain_Rate'] / 100 + player_data_clean['Avg_players']) * 100
    # print(twitch_data_clean)
    # print(player_data_clean)
    # sns.relplot(data=player_data_clean, x='year-month', y='Popularity_Score', kind='line', hue='Game_Name')
    # plt.title("Popularity Score")
    # plt.xlabel("2017 - 2021")
    # plt.xticks([])
    # plt.ylabel("Popularity Score")
    # plt.show()
    # Calculate influence score(streaming dataset), (hours watched / normalization base(100,000) + ((peak - avg) * weight(.5) + avg)/normalization base(100,000))
    
    twitch_data_clean['Influence_Score'] = np.log(twitch_data_clean['Hours_watched']) + ((twitch_data_clean['Peak_viewers'] -
                                                     twitch_data_clean['Avg_viewers']) / 100 + twitch_data_clean['Avg_viewers']) / 100
    # Calculate correlation between popularity and infleunce score, df.corr()
    # Correlation answers Research qs 2
    merged_scores = merge_data(twitch_data_clean, player_data_clean)
    merged_corr = merged_scores['Popularity_Score'].corr(merged_scores['Influence_Score'])
    # print(merged_corr)

    # Merge popularity and developer dataset, Calculate popularity score per developer employee, popularity score/# of employee
    # per developer answers Research qs 3
    player_data_agg = player_data_clean.groupby('Game_Name', as_index = False)['Popularity_Score'].mean()
    merged_developer = player_data_agg.merge(developer_data, left_on='Game_Name', right_on='Game')
    merged_developer['Popularity Per Employee'] = merged_developer['Popularity_Score'] / merged_developer['Employee Count']
    print(merged_developer)

    # Plot time series for each calculation
    fig, ax1 = plt.subplots(figsize=(12,6))
    sns.lineplot(data = merged_developer, x='Game_Name', y='Popularity Per Employee', ax=ax1)
    ax2 = ax1.twinx()
    sns.barplot(data = merged_developer, x='Game_Name', y='Popularity_Score', ax=ax2)
    plt.title("Popularity Score per Employee")
    plt.xlabel("Game")
    plt.xticks(rotation=45)
    plt.ylabel("Popularity Score")
    plt.show()
    # Perform analysis, generate visualizations, and interpret results
    # For example, you can plot correlations, trends, etc.
    # You can use libraries like matplotlib or seaborn
    
if __name__ == '__main__':
    main()
