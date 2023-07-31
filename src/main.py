import pandas as pd
import argparse
import sys


def read_cosine_reducer(file):
    reducer_output = []

    try:
        with open(file, 'r') as f:
            for line in f:
                line = line.strip().split("\t", 1)

                MovieData = line[0].strip("[()]").split(",")
                Movies1 = str(MovieData[0])
                Movies2 = str(MovieData[1])
                Rating = float(line[1])

                reducer_output.append(Movies1, Movies2, Rating)

        df = pd.DataFrame(reducer_output, columns=["MovieTitle_1", "MovieTitle_2", "Similarity"])
    except:
        sys.exit(f'file of {file} cant be open...')
    return df


def find_similar_movies(df, movie_title, num_recommend):
    movie_filtered = df[df["MovieTitle_1"].str.contains(movie_title, case=False)]
    movie_filtered = movie_filtered.sort_values(by="Similarity", ascending=False)
    recommendation = movie_filtered.head(num_recommend)[["MovieTitle_2"]]
    return recommendation


if __name__ == "__main__":
    
    # Accept Input
    parser = argparse.ArgumentParser(description='Movie Recommendation Search.')
    parser.add_argument('-CosineSim_Reducer', required=True, type=str, help='file output of the CosineSimilarity Reducer')
    parser.add_argument('-Search_Movie', required=True, type=str, help='search MovieTitle')
    parser.add_argument('-Num_Recommend', required=True, type=str, help='number of recommendations to output')
    args = parser.parse_args()

    df = read_cosine_reducer(args.CosineSim_Reducer)
    print(find_similar_movies(df, args.Search_Movie, args.Num_Recommend))
