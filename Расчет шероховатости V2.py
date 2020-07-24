# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 21:10:08 2020

@author: Andrey
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, uniform_filter, iterate_structure,  grey_opening, grey_closing
import math

#[PROFILE_HEADER]
#NAME=/var/opt//Mahr/ps10/results/Profiles/VRLM.304425.004.003_2020-03-02_17-14-29.txt
interval_lin = 'INTERVAL_LIN '
pretrav_lin = 'PRETRAV_LIN '
posttrav_lin = 'POSTTRAV_LIN '
no_points = 'NO_POINTS '
start_x = 'START_X '
stop_x = 'STOP_X '
#[PROFILE_HISTORY]
ProductName = "ProductName "
ProductVersion = 'ProductVersion '
MachineName = 'MachineName '
MachineNumber = 'MachineNumber '
ProbeName = 'ProbeName '
VLIN = 'VLIN '
DateTime = 'DateTime '
profile_values = '[PROFILE_VALUES]'
sigma1 = 200


def s_x (Y, lambda_c):
    alfa = np.sqrt((math.log(2)/math.pi) )
    Lc = 0.5
    
    if (-L*lambda_c <= Y or Y <= Lc * lambda_c): 
        s_x = 1/(alfa*lambda_c)*math.exp(-math.pi * (Y/(alfa*lambda_c))**2)
    else:
        s_x = 0
    return s_x

name_file = "D:\VRLM.304425.004.003_2020-03-02_17-17-20.txt"
data_file = open(name_file).read().replace('=', ' ')

n = int(5) #Количество интервалов

start = data_file[data_file.find(pretrav_lin)+len(pretrav_lin):data_file.find(pretrav_lin)+len(pretrav_lin)+8]
stop_x_val = data_file[data_file.find(stop_x)+len(stop_x):data_file.find(stop_x)+len(stop_x)+8]
stop = round(float(stop_x_val) - float(data_file[data_file.find(posttrav_lin)+len(posttrav_lin):data_file.find(posttrav_lin)+len(posttrav_lin)+8]),6)
N_points = int(data_file[data_file.find(no_points)+len(no_points):data_file.find(no_points)+len(no_points)+4])



data = data_file[data_file.find(profile_values)+len(profile_values)+1::].split('\n')
dt1 = [('№', 'i2'), ('X', 'f4'), ('Y', 'f4'), ('Z', 'f4')]

a = np.genfromtxt(data, dtype=dt1)
list_x = list(a['X'])

interval_start = int(float(start)/(float(stop_x_val)/int(N_points)))
interval_stop = int(float(stop)/(float(stop_x_val)/int(N_points)))
L = stop - float(start)
lambda_c = L/n*100

b = a[::][interval_start: interval_stop] #Интервал для расчетов шероховатости без участка разгона и торможения
c = np.split(b, n)
b_gaus = gaussian_filter(b['Y'], sigma=sigma1).T
c_gaus = np.split(b_gaus, n)


for i in range(0, n):
    c[i]['Y'] = c[i]['Y']-c_gaus[i]

plt.subplots(figsize=(40,3))
plt.title('Фактический профиль')
for i in range(0, n):
    plt.plot(c[i]['X'], c[i]['Y'])

for i in range(0, len(b)):
    a = s_x(b['Y'][i], lambda_c)

    print(a)