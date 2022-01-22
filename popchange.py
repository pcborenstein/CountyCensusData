import requests
import re
import matplotlib.pyplot as plt
import numpy as np

#get the states
#response = requests.get("https://api.census.gov/data/2010/dec/sf1?get=NAME&for=state:*")
#
#states = re.split(",?\\n",response.text)
##skip the title
#states = states[1:]
#
#stateDict = {}
#
#for i in states:
#    matches = re.findall("\".*?\"",i)
#    stateDict[matches[1]] = matches[0]

response = requests.get("https://api.census.gov/data/2010/dec/sf1?get=P001001,NAME&for=combined statistical area:*")

MSAs = re.split(",?\\n",response.text)
#skip the title
MSAs = MSAs[1:]
MSAnames = {}
MSApop = {}
mergedList = []

for MSA in MSAs:
    matches = re.findall("\"(.*?)(?:\sCSA)?\"",MSA)
    MSAnum = int(matches[2])
    pop = int(matches[0])
    name = matches[1]
    #if(pop > 1.5e6):
    MSApop[MSAnum] = int(pop)
    MSAnames[MSAnum] = name
    mergedList.append((pop,name,MSAnum))


response = requests.get("https://api.census.gov/data/2020/dec/pl?get=P1_001N,NAME&for=combined%20statistical%20area:*")


MSApop2020 = {}
MSAs = re.split(",?\\n",response.text)
MSAs = MSAs[1:]
mergedList2020 = []

gain2020 = np.arange(1,19)
loss2020 = np.arange(1,19)


for MSA in MSAs:
    matches = re.findall("\"(.*?)\"",MSA)
    MSAnum = int(matches[2])
    MSApop2020[MSAnum] = int(matches[0])
    mergedList2020.append((pop,name,MSAnum))

sortedList = sorted(mergedList, reverse=True)[:20]

#

#ml = MSApop.items()
#ml = sorted(ml)
#x , pops = zip(*ml)
#ml = MSAnames.items()
#x , names = zip(*ml)
names = [0] * len(sortedList) 
pops = [0] * len(sortedList) 
pops2020 = [0] * len(sortedList) 
for i in range(len(sortedList)):
    pops[i] = sortedList[i][0]
    names[i] = sortedList[i][1]
    pops2020[i] = MSApop2020[sortedList[i][2]]

pops.reverse()
pops2020.reverse()
names.reverse()

gain2020 = [0] * len(sortedList) 
loss2020 = [0] * len(sortedList) 

for i in range(len(sortedList)):
    if(pops2020[i] >= pops[i]):
        gain2020[i] = pops2020[i]
        loss2020[i] = 0
    else:
        gain2020[i] = 0
        loss2020[i] = pops2020[i]

plt.figure(figsize=(15,8))
plt.title("MSA Growth 2010 to 2020")
plt.barh(names, gain2020, color = 'C2')
plt.barh(names, pops)
plt.barh(names, loss2020, color = 'C3')
ax = plt.gca()

colors = {'2010 Population':'C0', '2020 Decline':'C3', '2020 Growth':'C2'}
labels = list(colors.keys())
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
plt.legend(handles, labels)

#ax.set_yticks(base)
#ax.set_yticklabels(ageStr)

plt.grid(axis='x', linestyle=(0,(2,10)))

ax = plt.gca()
fig= plt.gcf()
plt.tight_layout()
plt.show()
