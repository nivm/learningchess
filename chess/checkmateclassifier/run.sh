cat ../../data/IB1419.pgn | python ./process_data.py
cat ../../data/results/checkmateclassifier/input | python feature_extraction.py > ../../data/results/checkmateclassifier/input_features.tsv
