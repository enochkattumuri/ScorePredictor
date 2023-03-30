import pandas as pd;
from pathlib import Path;

# add path to dataset here
PATH_TO_DATASET = '';
dataset = pd.read_csv(PATH_TO_DATASET);

# Columns: ['match_id', 'ball', 'runs_off_bat', 'extras', 'wicket_type', 'other_wicket_type']

# drop unnecessary columns
dataset.drop(
    columns=['ball', 'wicket_type', 'other_wicket_type'],
    inplace=True,
);

# Columns: ['match_id', 'runs_off_bat', 'extras']

MATCH_ID_COL = 0;
RUNS_OFF_BAT_COL = 1;
EXTRAS_COL = 2;

def runsScored(runsOffBat, extras):
    return int(runsOffBat + extras);

def addRunsScored(data):
    runsScoredCol = [0] * len(data);
    for i in range(len(data)):
        runsScoredCol[i] = runsScored(
            *data.iloc[i, [RUNS_OFF_BAT_COL,EXTRAS_COL]].values
        );
    return runsScoredCol;

print('Adding runs scored column ...');
dataset['runs_scored'] = addRunsScored(dataset);
print('Done ...');

RUNS_SCORED_COL = 3; # new column added at the end

################################################################################

score = 0;

def resetScore():
    global score;
    score = 0;

def computeScore(data):
    global score;
    prevMatchId = data.iloc[0, [MATCH_ID_COL]].values[0];
    scoreCol = [0] * len(data);
    for i in range(len(data)):
        matchId = data.iloc[i, [MATCH_ID_COL]].values;
        # check if match has changed
        if (matchId != prevMatchId):
            prevMatchId = matchId;
            resetScore();
        score += data.iloc[i, [RUNS_SCORED_COL]].values[0];
        scoreCol[i] = int(score);
    return scoreCol;

print('Adding score column ...');
dataset['score'] = computeScore(dataset);
print('Done ...');

SCORE_COL = 4; # new column added at the end

################################################################################

def computeTeamTotal(data):
    prevMatchId = data.iloc[0, [MATCH_ID_COL]].values[0];
    teamTotalCol = [None] * len(data);
    for i in range(len(data)):
        matchId = data.iloc[i, [MATCH_ID_COL]].values;
        # check if match has changed
        if (matchId != prevMatchId):
            prevMatchId = matchId;
            teamTotalCol[i-1] = int(data.iloc[i-1, [SCORE_COL]].values[0]);
    # for the last match
    teamTotalCol[i] = int(data.iloc[i, [SCORE_COL]].values[0]);
    return teamTotalCol;

def processTeamTotalCol(list):
    list.reverse();
    for i in range(len(list)):
        if list[i] is None:
            list[i] = list[i-1];
    list.reverse();
    return list;

print('Computing team total column ...');
teamTotalList = computeTeamTotal(dataset);
dataset['team_total'] = processTeamTotalCol(teamTotalList);
print('Done ...');

TEAM_TOTAL_COL = 5;

################################################################################

def computeRunsScoredTillNow(data):
    prevMatchId = data.iloc[0, [MATCH_ID_COL]].values[0];
    runsScoredTillNowCol = [0] * len(data);
    for i in range(1, len(data)):
        matchId = data.iloc[i, [MATCH_ID_COL]].values;
        # check if match has changed
        if (matchId != prevMatchId):
            prevMatchId = matchId;
            runsScoredTillNowCol[i] = 0;
            continue;
        runsScoredTillNowCol[i] = data.iloc[i-1, [SCORE_COL]].values[0];
    return runsScoredTillNowCol;

print('Adding runs scored till now column ...');
dataset['runs_scored_till_now'] = computeRunsScoredTillNow(dataset);
print('Done ...');

################################################################################

def getRunsScoredFromNow(runsScored, score, teamTotal):
    return int(teamTotal - score + runsScored);

def computeRunsScoredFromNow(data):
    runsScoredFromNowCol = [0] * len(data);
    for i in range(len(data)):
        runsScoredFromNowCol[i] = getRunsScoredFromNow(
            *data.iloc[i, [RUNS_SCORED_COL,SCORE_COL,TEAM_TOTAL_COL]].values
        );
    return runsScoredFromNowCol;

print('Adding runs scored from now column ...');
dataset['runs_scored_from_now'] = computeRunsScoredFromNow(dataset);
print('Done ...');

################################################################################

# drop columns with data of wickets
dataset.drop(
    columns=['runs_off_bat', 'extras', 'runs_scored', 'score', 'team_total'],
    inplace=True
);

# save csv with 'runs_scored_till_now' & 'runs_scored_from_now' columns
filepath = Path('./with_runs.csv');
dataset.to_csv(filepath, index=False);
