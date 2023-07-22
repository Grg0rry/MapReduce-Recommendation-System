import pandas as pd
import argparse


def parse_movie_title(input_file):
    """
    Convert the movie_titles.csv to dataframe and fix any bad lines

    Args:
    - input_file (str): The filepath of movie_titles.csv

    Returns:
    - df (dataframe) of the movie_titles.
    """

    def handle_bad_lines(line):
        fields =[str(field) for field in line]
        MovieID = int(fields[0])
        ReleaseYear = int(fields[1])
        MovieTitle = ''.join(fields[2:]).strip()
        return MovieID, ReleaseYear, MovieTitle
    
    df = pd.read_csv(input_file, names = ['MovieID', 'ReleaseYear', 'MovieTitle'], encoding='ISO-8859-1', engine='python', on_bad_lines=handle_bad_lines)
    return df


if __name__ == '__main__':
    
    # Accept Input
    parser = argparse.ArgumentParser(description='Preprocessing of MovieTitles CSV file.')
    parser.add_argument('-input', required=True, type=str, help='movie_titles.csv file')
    parser.add_argument('-output', required=True, type=str, help='Output CSV file')
    args = parser.parse_args()

    # Call function
    titles_df = parse_movie_title(args.input)
    titles_df.to_csv(args.output, index=False)
