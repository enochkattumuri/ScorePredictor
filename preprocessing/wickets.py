import pandas as pd;
from pathlib import Path;

# add path to dataset here
PATH_TO_DATASET = '';
dataset = pd.read_csv(PATH_TO_DATASET);

# Columns: ['match_id', 'ball', 'runs_off_bat', 'extras', 'wicket_type', 'other_wicket_type']

# drop unnecessary columns
dataset.drop(
    columns=['ball', 'runs_off_bat', 'extras'],
    inplace=True,
)

# Columns: ['match_id', 'wicket_type', 'other_wicket_type']

MATCH_ID_COL = 0;
WICKET_COL = 1;
OTHER_WICKET_COL = 2;

# add wickets in hand column
prevWicketsInHand = 10;

# get wickets in hand, if wicket or other wicket type is a valid value
def getWicketsInHand(wicket, otherWicket):
    global prevWicketsInHand;
    if (not pd.isna(wicket) or not pd.isna(otherWicket)):
        wicketsInHand = prevWicketsInHand;
        prevWicketsInHand -= 1;
        return wicketsInHand;
    return prevWicketsInHand;

# reset wickets in hand
def resetWicketsInHand():
    global prevWicketsInHand;
    prevWicketsInHand = 10;

# add wickets in hand column to the dataset
def addWicketsInHand(data):
    prevMatchId = data.iloc[0, [MATCH_ID_COL]].values[0];
    wicketsInHandCol = [0] * len(data);
    for i in range(len(data)):
        matchId = data.iloc[i, [MATCH_ID_COL]].values;
        # check if match has changed
        if (matchId != prevMatchId):
            prevMatchId = matchId;
            resetWicketsInHand();
        wicketsInHandCol[i] = getWicketsInHand(
            *data.iloc[i, [WICKET_COL,OTHER_WICKET_COL]].values
        );
    return wicketsInHandCol;

print('Adding wickets in hand column ...');
dataset['wickets_in_hand'] = addWicketsInHand(dataset);
print('Done ...');

# drop columns with data of wickets
dataset.drop(
    columns=['wicket_type', 'other_wicket_type'],
    inplace=True
);

# save csv with `wickets_in_hand` column
filepath = Path('./with_wickets_in_hand.csv');
dataset.to_csv(filepath, index=False);
