import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from data_processing import cleanse_twitch_data, cleanse_player_data, merge_data

def popularity_analysis(player_data: pd.DataFrame) -> None:
    # Calculate popularity score (popularity dataset), numpy.log((peak - avg) * gain rate / 100 + avg)
    # Popularity score answers Research qs 1
    player_data['Popularity_Score'] = np.log((player_data['Peak_Players'] - player_data['Avg_players']) *
                                            player_data['Gain_Rate'] / 100 + player_data['Avg_players']) * 100
    
    agg_populairty = player_data.groupby(['Game_Name'], as_index=False)['Popularity_Score'].mean()
    print(agg_populairty.sort_values(by=['Popularity_Score'], ascending=False))

    fig, ax1 = plt.subplots(figsize=(10,6))
    sns.lineplot(data=player_data, x='year', y='Popularity_Score', hue='Game_Name', ax=ax1)
    plt.title("Popularity Score")
    plt.xlabel("Year")
    plt.xticks([2017, 2018, 2019, 2020, 2021])
    plt.ylabel("Popularity Score")
    plt.axhline(y=1100, color='black') # Popularity Score = 1100 divides popularity of 10 sample games
    plt.show()

def influence_analysis(twitch_data: pd.DataFrame, player_data: pd.DataFrame) -> None:
    # Calculate influence score(streaming dataset), numpy.log((hours watched  + (peak - avg) / 100  + avg) /100   
    twitch_data['Influence_Score'] = np.log(twitch_data['Hours_watched']) + ((twitch_data['Peak_viewers'] -
                                            twitch_data['Avg_viewers']) / 100 + twitch_data['Avg_viewers']) / 100
    
    # Merge twitch_data and player_data
    # Calculate correlation between popularity score and infleunce score, df.corr()
    # Correlation answers Research qs 2
    merged_scores = merge_data(twitch_data, player_data)
    merged_corr = merged_scores['Popularity_Score'].corr(merged_scores['Influence_Score'])
    print(merged_corr) # Popularity and Influence Score correlation for all 10 games

    # Filter merged_scores to top 5 popular games
    merged_score_mean = player_data.groupby('Game_Name', as_index = False)['Popularity_Score'].mean()
    popular_game_filter = merged_score_mean[merged_score_mean['Popularity_Score'] > 1100]
    merged_score_popular = merged_scores[merged_scores['Game_Name'].isin(popular_game_filter['Game_Name'])]
    agg_score_popular = merged_score_popular.groupby(['Game_Name', 'year', 'month'], as_index=False).mean()

    # Plot Popularity Score vs Influence Score for top 5 games
    fig, ax1 = plt.subplots(figsize=(10,6))
    sns.lineplot(data = agg_score_popular, x='year', y='Popularity_Score', hue='Game_Name', ax=ax1)
    plt.xlabel("Year")
    plt.xticks([2017, 2018, 2019, 2020, 2021])
    plt.ylabel("Popularity Score")

    ax2 = ax1.twinx()
    sns.lineplot(data=merged_score_popular, x='year', y='Influence_Score', color='black', ax=ax2)
    plt.ylabel("Influence Score")
    plt.title("Popular Score vs Influence Score for Top 5 Popular Games")
    plt.show()

    merged_score_popular = merged_score_popular[['year', 'month', 'Popularity_Score', 'Influence_Score']]
    merged_corr_popular = merged_score_popular['Popularity_Score'].corr(merged_score_popular['Influence_Score'])
    print(merged_corr_popular) # Popularity and Influence Score correlation for top 5 popular games

    # Filter merged_scores to bottom 5 popular games
    unpopular_game_filter = merged_score_mean[merged_score_mean['Popularity_Score'] < 1100]
    merged_score_unpopular = merged_scores[merged_scores['Game_Name'].isin(unpopular_game_filter['Game_Name'])]
    # merged_score_unpopular = merged_score_unpopular[['year', 'month', 'Popularity_Score', 'Influence_Score']]
    agg_score_unpopular = merged_score_unpopular.groupby(['Game_Name', 'year', 'month'], as_index=False).mean()

    # Plot Popularity Score vs Influence Score for bottom 5 games
    fig, ax3 = plt.subplots(figsize=(10,6))
    sns.lineplot(data = agg_score_unpopular, x='year', y='Popularity_Score', hue='Game_Name', ax=ax3)
    plt.xlabel("Year")
    plt.xticks([2017, 2018, 2019, 2020, 2021])
    plt.ylabel("Popularity Score")

    ax4 = ax3.twinx()
    sns.lineplot(data=merged_score_unpopular, x='year', y='Influence_Score', color='black', ax=ax4)
    plt.ylabel("Influence Score")
    plt.title("Popular Score vs Influence Score for Bottom 5 Popular Games")
    plt.show()

    merged_score_unpopular = merged_score_unpopular[['year', 'month', 'Popularity_Score', 'Influence_Score']]
    merged_corr_unpopular = merged_score_unpopular['Popularity_Score'].corr(merged_score_unpopular['Influence_Score'])
    print(merged_corr_unpopular) # Popularity and Influence Score correlation for bottom 5 popular games


def developer_analysis(player_data: pd.DataFrame, developer_data: pd.DataFrame) -> None:
    # Merge popularity and developer dataset, Calculate popularity score per developer employee
    # per developer answers Research qs 3
    player_data_agg = player_data.groupby('Game_Name', as_index = False)['Popularity_Score'].mean()
    merged_developer = player_data_agg.merge(developer_data, left_on='Game_Name', right_on='Game')
    merged_developer['Popularity Per Employee'] = merged_developer['Popularity_Score'] / merged_developer['Employee Count']
    print(merged_developer)

    fig, ax1 = plt.subplots(figsize=(12,6))
    sns.barplot(data = merged_developer, x='Game_Name', y='Popularity_Score', ax=ax1)
    plt.xlabel("Game")
    plt.xticks(rotation='vertical')
    plt.ylabel("Popularity Score")
    plt.axhline(y=1100, color='black') # Popularity Score = 1100 divides popularity of 10 sample games

    ax2 = ax1.twinx()
    sns.lineplot(data = merged_developer, x='Game_Name', y='Popularity Per Employee', ax=ax2)
    plt.ylabel("Popularity Score Per Employee")
    plt.title("Popularity Score vs Popularity Per Employee")
    plt.show()


def main():
    # Load and preprocess all 3 datasets, Popularity dataset, Streaming dataset, developer dataset(pre-made)
    # path = '/Users/ethanzwang/Desktop/Cse_163_Project/'
    twitch_file = 'Twitch_game_data.csv'
    player_file = 'Valve_Player_Data.csv'
    developer_file = 'Game_Developer_Data.csv'

    twitch_data = pd.read_csv(twitch_file, encoding="cp1252")
    player_data = pd.read_csv(player_file, encoding="cp1252")
    developer_data = pd.read_csv(developer_file, encoding="cp1252")

    twitch_data_clean = cleanse_twitch_data(twitch_data)
    player_data_clean = cleanse_player_data(player_data)

    # Popularity Analysis - calculate and plot Popularity Score
    popularity_analysis(player_data_clean)
    
    # Influence Analysis - calculate Influence Score, merge 2 DataFrames
    # Calculate and plot the correlation between Popularity Score and Influence Score
    influence_analysis(twitch_data_clean, player_data_clean)

    # Developer Analysis - calculate and plot Popularity Score per employee
    developer_analysis(player_data_clean, developer_data)
    
if __name__ == '__main__':
    main()
