#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import random

ageStr = (
"under 5",
"5 to 9",
"10 to 14",
"15 to 19",
"20 to 24",
"25 to 29",
"30 to 34",
"35 to 39",
"40 to 44",
"45 to 49",
"50 to 54",
"55 to 59",
"60 to 64",
"65 to 69",
"70 to 74",
"75 to 79",
"80 to 84",
"85 and up"
)

#based on table S0101 - estimates do not use
#ageT11 = np.array([10.2,7.5, 5.3, 3.9, 12, 10.4, 11.3, 6, 8.1, 5.4, 6.9, 7.2, 1.7, 1.2, 1.4, 0, 1.5, 0])
#ageT11 *= 1474 / 100
#ageT11 = ageT11.round()
#
#ageT12 = np.array([2.6, 4.9, 8.2, 5, 4.4, 5.7, 14.9, 8.2, 6.5, 6.1, 7.6, 13.1, 3.8, 1.8, 2.5, 3.4,  1.0, 0.5 ])
#ageT12 *= 1981 / 100
#ageT12 = ageT12.round()

#updated for table P12 Sex by age
#2010: DEC SUmmary File1
ageT11_male = np.array([56,63,33,32,47,75,71,66,82,75,94,79,57,23,12,15,2,1])
ageT12_male = np.array([51,67,63,51,64,76,64,77,106,100,88,88,74,32,25,15,10,6])

ageT11_female = np.array([61,50,44,41,56,63,63,63,61,64,87,41,41,16,24,10,9,11])
ageT12_female = np.array([77,60,48,46,64,69,90,64,72,78,87,71,57,44,19,13,13,9])

ageT11 = ageT11_male + ageT11_female
ageT12 = ageT12_male + ageT12_female
ageTotal2010 = ageT11 + ageT12

ageTotal2020 = np.array([200]*18)

for i in np.arange(1,18):
    ageTotal2020[i] = ageTotal2010[i] + random.randint(-10,50)
    

base = np.arange(1,19)
gain2020 = np.arange(1,19)
loss2020 = np.arange(1,19)

for i in np.arange(1,18):
    if(ageTotal2020[i] >= ageTotal2010[i]):
        gain2020[i] = ageTotal2020[i]
        loss2020[i] = 0
    else:
        gain2020[i] = 0
        loss2020[i] = ageTotal2020[i]

#plt.barh(base, ageTotal)
#plt.barh(base, gain2020, color = 'C2')
plt.barh(base, ageTotal2010)
#plt.barh(base, loss2020, color = 'C3')
ax = plt.gca()

colors = {'2010 Population':'C0', '2020 Decline':'C3', '2020 Growth':'C2'}
labels = list(colors.keys())
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
plt.legend(handles, labels)

ax.set_yticks(base)
ax.set_yticklabels(ageStr)

plt.grid(axis='x', linestyle=(0,(2,10)))

plt.title("Springfield Population")
plt.show()
