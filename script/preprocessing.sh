#!/bin/bash
set -e
start=$(date +%s)

python3 ./preprocessing/RatingsPreprocessing.py \
-combinedData ./data/combined_data_1.txt,./data/combined_data_2.txt,./data/combined_data_3.txt,./data/combined_data_4.txt \
-output ./data/cleaned_ratings.csv
echo "task 1/3 done..."

python3 ./preprocessing/TitlesPreprocessing.py \
-input ./data/movie_titles.csv \
-output ./data/cleaned_titles.csv
echo "task 2/3 done..."

python3 ./preprocessing/CombineMovieTitles.py \
-ratings ./data/cleaned_ratings.csv \
-titles ./data/cleaned_titles.csv \
-output ./data/cleaned_moviesTitles.csv
echo "task 3/3 done..."
echo "output in ./data/cleaned_moviesTitles.csv"

end=$(date +%s)
total_time=$((end - start))
echo "Total time taken: $total_time seconds"