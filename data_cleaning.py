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

df_out.to_csv('combine_rookie_data_cleaned.csv', index=False)