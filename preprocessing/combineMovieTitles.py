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
    f = ['count','mean']
    df_movie_summary = movies_df.groupby('MovieID')['Rating'].agg(f)
    df_movie_summary.index = df_movie_summary.index.map(int)
    movie_benchmark = round(df_movie_summary['count'].quantile(0.7),0)
    drop_movie_list = df_movie_summary[df_movie_summary['count'] < movie_benchmark].index

    df_cust_summary = movies_df.groupby('UserID')['Rating'].agg(f)
    df_cust_summary.index = df_cust_summary.index.map(int)
    cust_benchmark = round(df_cust_summary['count'].quantile(0.7),0)
    drop_cust_list = df_cust_summary[df_cust_summary['count'] < cust_benchmark].index
    
    movies_df = movies_df[~movies_df['MovieID'].isin(drop_movie_list)]
    movies_df = movies_df[~movies_df['UserID'].isin(drop_movie_list)]

    # Save output
    movies_df = movies_df[['MovieTitle','UserID','Rating']]
    movies_df.to_csv(args.output, index=False, header=False)