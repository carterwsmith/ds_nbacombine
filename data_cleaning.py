#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 13:40:05 2020

@author: csmith
"""

import pandas as pd

df = pd.read_csv('combine_rookie_data.csv')

#remove non-players (-1 appended)
df = df[df['0'] != -1]
df = df.drop(columns=['0'])

#remove first/last names
df = df.drop(columns=['FIRST_NAME', 'LAST_NAME'])

#remove measurements marked with ft_in
df = df.drop(columns=['HEIGHT_WO_SHOES_FT_IN', 'HEIGHT_W_SHOES_FT_IN', 'WINGSPAN_FT_IN', 'STANDING_REACH_FT_IN'])

#remove irrelevant statistics
df = df.drop(columns=['GP', 'GS', 'LEAGUE_ID', 'MIN', 'PLAYER_AGE', 'PLAYER_ID_rookie', 'SEASON_ID', 'TEAM_ID'])

import numpy as np
from numpy import nan

#turn fractions into numerics
df_fracs_1 = df[['SPOT_FIFTEEN_CORNER_LEFT', 'SPOT_FIFTEEN_BREAK_LEFT', 'SPOT_FIFTEEN_TOP_KEY', 'SPOT_FIFTEEN_BREAK_RIGHT', 'SPOT_FIFTEEN_CORNER_RIGHT']]
df_fracs_1 = df_fracs_1.applymap(lambda x: x.replace('-', '/') if pd.notnull(x) else x)
df_fracs_1 = df_fracs_1.apply(lambda x: pd.eval(x) if pd.notnull(x[0]) else x, axis=1)

df_fracs_2 = df[['SPOT_COLLEGE_CORNER_LEFT','SPOT_COLLEGE_BREAK_LEFT','SPOT_COLLEGE_TOP_KEY','SPOT_COLLEGE_BREAK_RIGHT','SPOT_COLLEGE_CORNER_RIGHT']]
df_fracs_2 = df_fracs_2.applymap(lambda x: x.replace('-', '/') if pd.notnull(x) else x)
df_fracs_2 = df_fracs_2.applymap(lambda x: pd.eval(x) if pd.notnull(x) else x)

df_fracs_3 = df[['SPOT_NBA_CORNER_LEFT', 'SPOT_NBA_BREAK_LEFT', 'SPOT_NBA_TOP_KEY', 'SPOT_NBA_BREAK_RIGHT', 'SPOT_NBA_CORNER_RIGHT']]
df_fracs_3 = df_fracs_3.applymap(lambda x: x.replace('-', '/') if pd.notnull(x) else x)
df_fracs_3 = df_fracs_3.applymap(lambda x: pd.eval(x) if pd.notnull(x) else x)

df_fracs_4 = df[['OFF_DRIB_FIFTEEN_BREAK_LEFT', 'OFF_DRIB_FIFTEEN_TOP_KEY', 'OFF_DRIB_FIFTEEN_BREAK_RIGHT', 'OFF_DRIB_COLLEGE_BREAK_LEFT', 'OFF_DRIB_COLLEGE_TOP_KEY']]
df_fracs_4 = df_fracs_4.applymap(lambda x: x.replace('-', '/') if pd.notnull(x) else x)
df_fracs_4 = df_fracs_4.stack(dropna=False).map(lambda x: pd.eval(x) if pd.notna(x) else x).unstack()

df_fracs_5 = df[['OFF_DRIB_COLLEGE_BREAK_RIGHT', 'ON_MOVE_FIFTEEN', 'ON_MOVE_COLLEGE']]
df_fracs_5 = df_fracs_5.applymap(lambda x: x.replace('-', '/') if pd.notna(x) else x)
df_fracs_5 = df_fracs_5.stack(dropna=False).map(lambda x: pd.eval(x) if pd.notna(x) else x).unstack()

all_fracs = [df_fracs_1, df_fracs_2, df_fracs_3, df_fracs_4, df_fracs_5]
df_numerics = pd.concat(all_fracs, axis=1)

df = df.drop(columns=['SPOT_FIFTEEN_CORNER_LEFT', 'SPOT_FIFTEEN_BREAK_LEFT', 'SPOT_FIFTEEN_TOP_KEY', 'SPOT_FIFTEEN_BREAK_RIGHT', 'SPOT_FIFTEEN_CORNER_RIGHT', 'SPOT_COLLEGE_CORNER_LEFT', 'SPOT_COLLEGE_BREAK_LEFT', 'SPOT_COLLEGE_TOP_KEY', 'SPOT_COLLEGE_BREAK_RIGHT', 'SPOT_COLLEGE_CORNER_RIGHT', 'SPOT_NBA_CORNER_LEFT', 'SPOT_NBA_BREAK_LEFT', 'SPOT_NBA_TOP_KEY', 'SPOT_NBA_BREAK_RIGHT', 'SPOT_NBA_CORNER_RIGHT', 'OFF_DRIB_FIFTEEN_BREAK_LEFT', 'OFF_DRIB_FIFTEEN_TOP_KEY', 'OFF_DRIB_FIFTEEN_BREAK_RIGHT', 'OFF_DRIB_COLLEGE_BREAK_LEFT', 'OFF_DRIB_COLLEGE_TOP_KEY', 'OFF_DRIB_COLLEGE_BREAK_RIGHT', 'ON_MOVE_FIFTEEN', 'ON_MOVE_COLLEGE'])
df = df.join(df_numerics)

#organize dataframe
def movecol(df, cols_to_move=[], ref_col='', place='After'):
    
    cols = df.columns.tolist()
    if place == 'After':
        seg1 = cols[:list(cols).index(ref_col) + 1]
        seg2 = cols_to_move
    if place == 'Before':
        seg1 = cols[:list(cols).index(ref_col)]
        seg2 = cols_to_move + [ref_col]
    
    seg1 = [i for i in seg1 if i not in seg2]
    seg3 = [i for i in cols if i not in seg1 + seg2]
    
    return(df[seg1 + seg2 + seg3])

df_out = movecol(df, 
             cols_to_move=['TEAM_ABBREVIATION'], 
             ref_col='PLAYER_NAME',
             place='Before')

df_out = movecol(df_out,
             cols_to_move=['SPOT_FIFTEEN_CORNER_LEFT', 'SPOT_FIFTEEN_BREAK_LEFT', 'SPOT_FIFTEEN_TOP_KEY', 'SPOT_FIFTEEN_BREAK_RIGHT', 'SPOT_FIFTEEN_CORNER_RIGHT', 'SPOT_COLLEGE_CORNER_LEFT', 'SPOT_COLLEGE_BREAK_LEFT', 'SPOT_COLLEGE_TOP_KEY', 'SPOT_COLLEGE_BREAK_RIGHT', 'SPOT_COLLEGE_CORNER_RIGHT', 'SPOT_NBA_CORNER_LEFT', 'SPOT_NBA_BREAK_LEFT', 'SPOT_NBA_TOP_KEY', 'SPOT_NBA_BREAK_RIGHT', 'SPOT_NBA_CORNER_RIGHT', 'OFF_DRIB_FIFTEEN_BREAK_LEFT', 'OFF_DRIB_FIFTEEN_TOP_KEY', 'OFF_DRIB_FIFTEEN_BREAK_RIGHT', 'OFF_DRIB_COLLEGE_BREAK_LEFT', 'OFF_DRIB_COLLEGE_TOP_KEY', 'OFF_DRIB_COLLEGE_BREAK_RIGHT', 'ON_MOVE_FIFTEEN', 'ON_MOVE_COLLEGE'],
             ref_col='BENCH_PRESS',
             place='After')

df_out.to_csv('combine_rookie_data_cleaned.csv', index=False)