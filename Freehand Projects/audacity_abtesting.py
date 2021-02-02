#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 19:24:33 2021

@author: babaniyiolaniyi

Data:  https://www.kaggle.com/samtyagi/audacity-ab-testing
Audacity AB Testing

"""

#____________ Import Packages ____________
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import * # bootstrap sampling
import statsmodels.api as sm
from scipy.stats import fisher_exact

#________________ 1. Data Exploration __________
# import data
df = pd.read_csv('homepage_actions.csv')
df = df.sort_values(by='id')
df.head()


# Count the number of unique users in each group
df_users = df.pivot_table(index='group', 
                          columns=['action'],
                          values = 'id', 
                          aggfunc='nunique',
                          margins = True)
                          
df_users 

ctr_control = round(df_users.loc['control','click']/df_users.loc['control','view'],2)
n_control_click = df_users.loc['control','click']
n_control_view = df_users.loc['control','view']

ctr = round(df_users.loc['All','click']/df_users.loc['All','view'],2)


ctr_expt = round(df_users.loc['experiment','click']/df_users.loc['experiment','view'],2)
n_expt_click = df_users.loc['experiment','click']
n_expt_view = df_users.loc['experiment','view']


print("CTR for control users:", ctr_control)
print("CTR for experiment users:", ctr_expt)


#______________ 2. Non-Parametric Method - Fisher's Exact Test ____________
'''
Fisher’s exact test is a non-parametric test that is often used as a substitute for 
    chi-square when the data set is small or categories are imbalanced.
    
In our case with the paying conversion, the categories are highly imbalanced: there are only
    28% – 31% of clicking users within test and control groups and the rest 70% are viewers, 
    so we can apply Fisher’s to check if the increase in CTR from 28% to 31% is actually 
    meaningful/significant.
    
Just as chi-square, Fisher’s test uses tables for all possible test values, but it
     calculates the exact probability of observing the distribution seen in the table
     (aka p-value) or even more extreme distribution, that’s why it is an “exact” test.

In this case, the null hypothesis is that the CTR among users in the experimental
    group is the same or less as in the control, and the alternative hypothesis is that it
    increased iin the control group.
'''


oddsratio, pvalue = fisher_exact([[n_control_click, n_control_view], [n_expt_click, n_expt_view]])

print("odd-ratio:", round(oddsratio,2))
print("Fishers exact test p-value:", round(pvalue,2))

if pvalue <= 0.05:
    print("H0 is rejected, the CTR new page > CTR old page, the increase is significant")
else:
    print("H0 is NOT rejected, the CTR new page <= CTR old page, there is no difference")

#_____________ 3. Parametric Method -  Sampling Distribution _____________

diffs = []
for i in tqdm(range(10000)):
    sample = df.sample(4000 ,replace = True)
    experiment_gr = sample.query("group == 'experiment'")
    control_gr = sample.query("group == 'control'")
    experiment_ctr = experiment_gr.query("action == 'click'").nunique()['id']/experiment_gr.query("action == 'view'").nunique()['id']
    control_ctr = control_gr.query("action == 'click'").nunique()['id']/control_gr.query("action == 'view'").nunique()['id']
    diffs.append( experiment_ctr - control_ctr)
    

# Plot a histogram of the p_diffs. Does this plot look like what you expected? 
# Use the matching problem in the classroom to assure you fully understand what was computed here.
'''
The simulated data creates a normal distribution (no skew) as expected due to how the data
was generated. The mean of this normal distribution is 0, which which is what the data
should look like under the null hypothesis.
'''
ctr_diff = ctr_expt - ctr_control
# Plot histogram
plt.hist(diffs)
plt.title('Simulated Difference of Experiment and Control CTR Under the Null')
plt.xlabel('CTR Difference')
plt.ylabel('Frequency')
plt.axvline(x=ctr_diff, color='r', linewidth=1, label="Real difference")
plt.axvline(x=(np.array(diffs).mean()), color='g', linestyle='dashed', linewidth=1, label="Simulated difference")
plt.legend()
plt.show()


# What proportion of the simulated diffs are greater than the actual difference observed in the original data?
# p-value as the percentage of simulations where the test statistic is at least as extreme as the observed difference in sample means.

ctr_diff = ctr_expt - ctr_control

# Find proportion of p_diffs greater than the actual difference
greater_than_diff = [i for i in diffs if i > ctr_diff]

# Calculate values
print("Actual difference:" , round(ctr_diff,2))

p_greater_than_diff = len(greater_than_diff)/len(diffs)

print('Proportion greater than actual difference (p-value):', p_greater_than_diff)

print('As a percentage (p-value): {}%'.format(p_greater_than_diff*100))



# null values
null_vals = np.random.normal(0 ,np.array(diffs).std() ,10000)

plt.hist(null_vals)
plt.axvline(x = np.array(null_vals).mean() ,color = 'yellow', label = 'Mean of null')
plt.axvline(x=ctr_diff, color='green', linewidth=1, label="Real difference")
plt.axvline(x=(np.array(diffs).mean()), color='red', linestyle='dashed', linewidth=1, label="Simulated difference")# we can see the observed stats are way out of the range of mean null vals
plt.legend()



#_____________ 3.2 Parametric - Ztest -----------


# Find z-score and p-value
z_score, p_value = sm.stats.proportions_ztest(count=[928, 932], 
                                              nobs=[3924, 4264])


if round(p-value,2) <= 0.05:
    print("H0 is rejected, the CTR new page > CTR old page, the increase is significant")
else:
    print("H0 is NOT rejected, the CTR new page <= CTR old page, there is no difference")

