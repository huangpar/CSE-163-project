import pandas as pd

from cse163_utils import assert_equals
from data_processing import cleanse_twitch_data, cleanse_player_data,\
                            merge_data


def test_cleanse_twitch_data(df: pd.DataFrame) -> None:
    """
    Test method cleanse_twitch_data
    """
    processed_data = cleanse_twitch_data(df)

    assert_equals(500, processed_data.shape[0])
    assert_equals(6, processed_data.shape[1])
    assert_equals(0, processed_data[processed_data['Year'] < 2017].shape[0])
    assert_equals(0, processed_data[processed_data['Year'] > 2021].shape[0])
    assert_equals(10, processed_data['Game'].nunique())


def test_cleanse_player_data(df: pd.DataFrame) -> None:
    """
    Test method cleanse_player_data
    """
    processed_data = cleanse_player_data(df)

    assert_equals(475, processed_data.shape[0])
    assert_equals(7, processed_data.shape[1])
    assert_equals(int, processed_data['month'].dtypes)
    assert_equals(int, processed_data['year'].dtypes)
    assert_equals(0, processed_data[processed_data['year'] < 2017].shape[0])
    assert_equals(0, processed_data[processed_data['year'] > 2021].shape[0])
    assert_equals(10, processed_data['Game_Name'].nunique())
    assert_equals(False, processed_data['Gain_Rate'].isna().any())


def test_merge_data(df1: pd.DataFrame, df2: pd.DataFrame) -> None:
    """
    Test method merge_data
    """
    processed_data = merge_data(df1, df2)

    assert_equals(451, processed_data.shape[0])
    assert_equals(3, processed_data.shape[1])
    assert_equals(False, 'Year' in processed_data.columns)
    assert_equals(True, 'year' in processed_data.columns)


def main():
    twitch_file = 'Twitch_game_data.csv'
    player_file = 'Valve_Player_Data.csv'
    # developer_file = 'Game_Developer_Data.csv'

    twitch_data = pd.read_csv(twitch_file, encoding="cp1252")
    player_data = pd.read_csv(player_file, encoding="cp1252")
    # developer_data = pd.read_csv(developer_file, encoding="cp1252")

    test_cleanse_twitch_data(twitch_data)
    test_cleanse_player_data(player_data)
    test_merge_data(cleanse_twitch_data(twitch_data),
                    cleanse_player_data(player_data))


if __name__ == '__main__':
    main()
