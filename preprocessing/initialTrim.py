import pandas as pd;
from pathlib import Path;

# add path to dataset here
PATH_TO_DATASET = '';
dataset = pd.read_csv(PATH_TO_DATASET);

# print the shape and labels of a given dataset
def viewShape(dataset):
    print(dataset.shape);
    print(dataset.columns);

# viewShape(dataset);
# (225954, 22)

# Columns:
# ['match_id', 'season', 'start_date', 'venue', 'innings', 'ball',
# 'batting_team', 'bowling_team', 'striker', 'non_striker', 'bowler',
# 'runs_off_bat', 'extras', 'wides', 'noballs', 'byes', 'legbyes', 'penalty',
# 'wicket_type', 'player_dismissed', 'other_wicket_type',
# 'other_player_dismissed'],

# Removing unwanted columns
# Match Details
matchDetails = [
    'season',
    'start_date',
    'venue',
    'batting_team',
    'bowling_team'
];

# Player Details
playerDetails  = [ 'striker', 'non_striker', 'bowler'];

# Scoring Details
scoringDetails = [
    'wides',
    'noballs',
    'byes',
    'legbyes',
    'penalty'
];

# Wicket Details
wicketDetails = [ 'player_dismissed', 'other_player_dismissed'];

# Drop columns which are not needed
dataset.drop(
    columns=[ *matchDetails, *playerDetails, *scoringDetails, *wicketDetails],
    inplace=True
);

# viewShape(dataset);
# (225954, 7)

# Removing unwanted rows
# Remove all rows with data of 2nd innings
dataset = dataset[dataset['innings'] != 2];

# dropping innings column
dataset.drop(columns=[ 'innings'], inplace=True);

# viewShape(dataset);
# (117044, 6)
# Columns: ['match_id', 'ball', 'runs_off_bat', 'extras', 'wicket_type', 'other_wicket_type']

filepath = Path('../dataset/initialTrim.csv');
dataset.to_csv(filepath, index=False);
