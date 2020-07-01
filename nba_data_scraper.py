#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 15:09:58 2020

@author: csmith
"""
import pandas as pd
from nba_api.stats.endpoints import DraftCombineStats
import time

df14 = DraftCombineStats('00', '2014-15').get_data_frames()[0]
time.sleep(.6)
df15 = DraftCombineStats('00', '2015-16').get_data_frames()[0]
time.sleep(.6)
df16 = DraftCombineStats('00', '2016-17').get_data_frames()[0]
time.sleep(.6)
df17 = DraftCombineStats('00', '2017-18').get_data_frames()[0]
time.sleep(.6)
df18 = DraftCombineStats('00', '2018-19').get_data_frames()[0]
time.sleep(.6)

combine = [df14,df15,df16,df17,df18]
df_combine = pd.concat(combine, ignore_index=True)

from nba_api.stats.endpoints import PlayerCareerStats
num = 0
df_rookie_stats = pd.DataFrame()

while num<len(df_combine.index):
    player_id = df_combine.at[num, 'PLAYER_ID']
    try:
        time.sleep(.5)
        rookie_stats = PlayerCareerStats(player_id, 'PerGame', '00').get_data_frames()[0].head(1)
        time.sleep(.5)
        if rookie_stats.at[0, 'GP'] < 10:
            df_rookie_stats = df_rookie_stats.append(rookie_stats, ignore_index=True)
        else:
            time.sleep(.5)
            df_rookie_stats = df_rookie_stats.append(PlayerCareerStats(player_id, 'PerGame', '00').get_data_frames()[0].head(1), ignore_index=True)
    except:
        time.sleep(.5)
        df_rookie_stats = df_rookie_stats.append(pd.DataFrame([-1]), ignore_index=True)    
    num+=1
    
df_final = df_combine.join(df_rookie_stats, lsuffix='_combine', rsuffix='_rookie')