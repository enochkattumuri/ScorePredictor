import pandas as pd;
from pathlib import Path;

wickets = pd.read_csv('./with_wickets_in_hand.csv');
balls = pd.read_csv('./with_balls_left.csv');
runs = pd.read_csv('./with_runs.csv');

# def viewShape(dataset):
#     print(dataset.shape);
#     print(dataset.columns);

dataset = balls;
dataset['wickets_in_hand'] = wickets['wickets_in_hand'];
dataset['runs_scored_till_now'] = runs['runs_scored_till_now'];
dataset['runs_scored_from_now'] = runs['runs_scored_from_now'];

dataset.drop(columns=['match_id'], inplace=True);

# viewShape(dataset);

# save final csv
filepath = Path('../ipl_final.csv');
dataset.to_csv(filepath, index=False);
