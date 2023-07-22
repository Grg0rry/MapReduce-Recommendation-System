#!/bin/bash
start=$(date +%s)

python3 ./preprocessing/ratingsPreprocessing.py \
-combinedData ./data/combined_data_1.txt,./data/combined_data_2.txt,./data/combined_data_3.txt,./data/combined_data_4.txt \
-output ./data/cleaned_ratings.csv

python3 ./preprocessing/titlesPreprocessing.py \
-input ./data/movie_titles.csv \
-output ./data/cleaned_titles.csv

python3 ./preprocessing/combineMovieTitles.py \
-ratings ./data/cleaned_ratings.csv \
-titles ./data/cleaned_titles.csv \
-output ./data/cleaned_moviesTitles.csv

split -b 1G ./data/cleaned_moviesTitles.csv ./data/cleaned_moviesTitles/

end=$(date +%s)
total_time=$((end - start))
echo "Total time taken: $total_time seconds"