# -*- coding: utf-8 -*-
"""
Hydropy package

@author: Stijn Van Hoey
"""
from __future__ import absolute_import, print_function

import numpy as np
import pandas as pd
# TOSO: nose2 wasn't finding seaborn
#import seaborn as sns
#sns.set_style('whitegrid')
import matplotlib.pyplot as plt

from hydropy.flowanalysis import HydroAnalysis
from hydropy.storm import selectstorms, plotstorms

flowdata = pd.read_pickle("data/FlowData")
raindata = pd.read_pickle("data/RainData")
flow2use = flowdata["L06_347"]

#%%
myflowserie = HydroAnalysis(flowdata)#, datacols=['LS06_342'])
myflowserie_short = myflowserie['LS06_347'].get_year("2010")

#%%
# Select the summer of 2009:
myflowserie.get_year('2009').get_season("Summer").plot(figsize=(12,6))

#%% Select all June data
flow_june = myflowserie.get_month("Jun")
flow_june_df = flow_june.get_data_only()

#%%  recession in June 2010
myflowserie.get_year('2011').get_month("Jun").get_recess().plot(figsize=(12,6))

#%%
fig, ax = plt.subplots(figsize=(13, 6))
myflowserie['LS06_347'].get_year('2010').get_month("Jul").get_highpeaks(150, above_percentile=0.9).plot(style='o', ax=ax)
myflowserie['LS06_347'].get_year('2010').get_month("Jul").plot(ax=ax)

#%%
fig, ax = plt.subplots(figsize=(13, 6))
myflowserie['LS06_347'].get_year('2010').get_month("Jul").get_lowpeaks(50, below_percentile=1.).plot(style='o', ax=ax)
myflowserie['LS06_347'].get_year('2010').get_month("Jul").plot(ax=ax)

#%% STORMS

#function can be used on pd.Series
stormfun = selectstorms(flowdata['LS06_347'], raindata['P05_039'],
                        number_of_storms = 3, drywindow = 96)
plotstorms(flowdata['LS06_347'], raindata['P05_039'], stormfun,
               make_comparable = False,
               period_title = True)

#%%implemented in the HydroAnalysis:
storms = myflowserie.derive_storms(raindata['P06_014'], 'LS06_347',
                                   number_of_storms=3, drywindow=96,
                                   makeplot=True)

#%% READY MADE FOR UNIT TEST PURPOSES

