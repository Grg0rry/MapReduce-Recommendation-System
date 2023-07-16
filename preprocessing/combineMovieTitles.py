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
    ratings_df = pd.read_csv(args.ratings)
    titles_df = pd.read_csv(args.titles)

    # Compile and Output csv
    movies_df = pd.merge(ratings_df, titles_df, how="left", on="MovieID")
    movies_df.to_csv(args.output, index=False, header=False)