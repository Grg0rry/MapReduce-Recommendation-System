import pandas as pd
import argparse

if __name__ == '__main__':
    
    # Accept Input
    parser = argparse.ArgumentParser(description='Combine ratings and titles into a single CSV file through joining MovieID.')
    parser.add_argument('-ratings', required=True, type=str, help='movieRatings file')
    parser.add_argument('-titles', required=True, type=str, help='movieTitles file')
    parser.add_argument('-output', required=True, type=str, help='Output CSV file')
    args = parser.parse_args()

    # Call function
    ratings_df = pd.read_csv(args.ratings)[['UserID', 'Rating', 'RatingDate', 'MovieID']]
    titles_df = pd.read_csv(args.titles)[['MovieID', 'ReleaseYear', 'MovieTitle']]

    # Merge dataframe
    movies_df = pd.merge(ratings_df, titles_df, how="left", on="MovieID")

    # Remove duplicates
    movies_df.drop_duplicates(inplace=True)

    # Data slicing
    movie_quantile = movies_df['MovieID'].quantile(0.7)
    ovie_counts = movies_df['MovieID'].value_counts()
    drop_movie_list = movies_df[movies_df < movie_quantile].index
    movies_df = movies_df[~movies_df['MovieID'].isin(drop_movie_list)]

    # Save output
    movies_df = movies_df[['MovieTitle','UserID','Rating']]
    movies_df.to_csv(args.output, index=False, header=False)