import pandas as pd;
from pathlib import Path;

# add path to dataset here
PATH_TO_DATASET = '';
dataset = pd.read_csv(PATH_TO_DATASET);

# Columns: ['match_id', 'ball', 'runs_off_bat', 'extras', 'wicket_type', 'other_wicket_type']

# drop unnecessary columnds
dataset.drop(
    columns=['runs_off_bat', 'extras', 'wicket_type', 'other_wicket_type'],
    inplace=True
);

# Columns: ['match_id', 'ball']

MATCH_ID_COL = 0;

counter = 1;

def resetCounter():
    global counter;
    counter = 1;

def getBalls(data):
    global counter;
    prevMatchId = data.iloc[0, [MATCH_ID_COL]].values[0];
    ballsCol = [0] * len(data);
    for i in range(len(data)):
        matchId = data.iloc[i, [MATCH_ID_COL]].values;
        # check if match has changed
        if (matchId != prevMatchId):
            prevMatchId = matchId;
            resetCounter();
        ballsCol[i] = counter;
        counter += 1;
    return ballsCol;

print('Adding balls column ...');
dataset['balls'] = getBalls(dataset);
print('Done ...');

BALLS_COL = 2; # new column will be added at the end

def computeTotalBalls(data):
    prevMatchId = data.iloc[0, [MATCH_ID_COL]].values[0];
    totalBallsCol = [None] * len(data);
    for i in range(len(data)):
        matchId = data.iloc[i, [MATCH_ID_COL]].values;
        # check if match has changed
        if (matchId != prevMatchId):
            prevMatchId = matchId;
            totalBallsCol[i-1] = int(data.iloc[i-1, [BALLS_COL]].values[0]);
    # for the last match
    totalBallsCol[i] = int(data.iloc[i, [BALLS_COL]].values[0]);
    return totalBallsCol;

def processTotalBallsCol(list):
    list.reverse();
    for i in range(len(list)):
        if list[i] is None:
            list[i] = list[i-1];
    list.reverse();
    return list;

print('Adding total balls column ...');
totalBallsList = computeTotalBalls(dataset);
dataset['total_balls'] = processTotalBallsCol(totalBallsList);
print('Done ...');

TOTAL_BALLS_COL = 3; # new column will be added at the end

def ballsLeft(ball,total_balls):
    return int(total_balls - ball + 1);

def computeBallsLeftFromNow(data):
    ballsLeftFromNowCol = [0] * len(data);
    for i in range(len(data)):
        ballsLeftFromNowCol[i] = ballsLeft(
            *data.iloc[i, [BALLS_COL,TOTAL_BALLS_COL]].values
        );
    return ballsLeftFromNowCol;

print('Adding balls left column ...');
dataset['balls_left'] = computeBallsLeftFromNow(dataset);
print('Done ...');

# drop columns with data of balls and intermediate columns
dataset.drop(columns=['ball', 'balls', 'total_balls'], inplace=True);

# save csv with `balls_left` column
filepath = Path('./with_balls_left.csv');
dataset.to_csv(filepath, index=False);
