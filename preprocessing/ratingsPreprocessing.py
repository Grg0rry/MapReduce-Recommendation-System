import re
import pandas as pd
import argparse


def combine_movie_data(file):
    """
    Takes in input file(s) of combined_data_.txt data files and combine them to the
    structure of 'UserID'|'Rating'|'RatingDate'|'MovieID'

    Args:
    - file (str): The filepath of one combined_data.txt

    Returns:
    - df (dataframe) of the combined files.

    """
    pattern_MovieID = r'^(\d+):?\s*$'
    pattern_data = r'^(\d+),\s*([\d.]+)(?:,(.*))?$'

    data = []
    MovieID = None

    with open(file, 'r') as f:
        for line in f:
            line = line.strip()

            match_MovieID = re.match(pattern_MovieID, line)
            match_data = re.match(pattern_data, line)

            if match_MovieID:
                MovieID = int(match_MovieID.group(1))
            elif match_data:
                UserID = int(match_data.group(1))
                Rating = int(match_data.group(2))
                RatingDate = match_data.group(3)
                data.append([UserID, Rating, RatingDate, MovieID])
            else:
                raise Exception('Found neither MovieId nor Data')

    df = pd.DataFrame(data, columns=['UserID', 'Rating', 'RatingDate', 'MovieID'])
    return df


if __name__ == '__main__':
    
    # Accept Input
    parser = argparse.ArgumentParser(description='Preprocessing of input files into a CSV file.')
    parser.add_argument('-combinedData', required=True, type=str, help='combined_data_.txt file(s), separated by commas')
    parser.add_argument('-output', required=True, type=str, help='Output CSV file')
    args = parser.parse_args()

    # Call function
    ratings_df = pd.DataFrame(columns=['UserID', 'Rating', 'RatingDate', 'MovieID'])
    input_files = args.combinedData.split(',')
    for file in input_files:
        ratings_df = pd.concat([ratings_df, combine_movie_data(file)], ignore_index=True)

    ratings_df.to_csv(args.output, index=False)