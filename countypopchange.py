import requests
import re
import matplotlib.pyplot as plt
import numpy as np

abbrev = {"Alabama" : "AL", "Alaska" : "AK", "Arizona" : "AZ", "Arkansas" : "AR", "California" : "CA", "Colorado" : "CO", "Connecticut" : "CT", "Delaware" : "DE", "Florida" : "FL", "Georgia" : "GA", "Hawaii" : "HI", "Idaho" : "ID", "Illinois" : "IL", "Indiana" : "IN", "Iowa" : "IA", "Kansas" : "KS", "Kentucky" : "KY", "Louisiana" : "LA", "Maine" : "ME", "Maryland" : "MD", "Massachusetts" : "MA", "Michigan" : "MI", "Minnesota" : "MN", "Mississippi" : "MS", "Missouri" : "MO", "Montana" : "MT", "Nebraska" : "NE", "Nevada" : "NV", "New Hampshire" : "NH", "New Jersey" : "NJ", "New Mexico" : "NM", "New York" : "NY", "North Carolina" : "NC", "North Dakota" : "ND", "Ohio" : "OH", "Oklahoma" : "OK", "Oregon" : "OR", "Pennsylvania" : "PA", "Rhode Island" : "RI", "South Carolina" : "SC", "South Dakota" : "SD", "Tennessee" : "TN", "Texas" : "TX", "Utah" : "UT", "Vermont" : "VT", "Virginia" : "VA", "Washington" : "WA", "West Virginia" : "WV", "Wisconsin" : "WI", "Wyoming" : "WY", "Puerto Rico" : "PR"}


#cheat by adding previous queried results here
#asking for all counties from each state takes a while
countyPop2010 = [(9818605, 37, 'Los Angeles County', 6), (5194675, 31, 'Cook County', 17), (4092459, 201, 'Harris County', 48), (3817117, 13, 'Maricopa County', 4), (3095313, 73, 'San Diego County', 6), (3010232, 59, 'Orange County', 6), (2504700, 47, 'Kings County', 36), (2496435, 86, 'Miami-Dade County', 12), (2368139, 113, 'Dallas County', 48), (2230722, 81, 'Queens County', 36), (2189641, 65, 'Riverside County', 6), (2035210, 71, 'San Bernardino County', 6), (1951269, 3, 'Clark County', 32), (1931249, 33, 'King County', 53), (1820584, 163, 'Wayne County', 26), (1809034, 439, 'Tarrant County', 48), (1781642, 85, 'Santa Clara County', 6), (1748066, 11, 'Broward County', 12), (1714773, 29, 'Bexar County', 48), (1585873, 61, 'New York County', 36), (1526006, 101, 'Philadelphia County', 42), (1510271, 1, 'Alameda County', 6), (1503085, 17, 'Middlesex County', 25), (1493350, 103, 'Suffolk County', 36), (1418788, 67, 'Sacramento County', 6), (1385108, 5, 'Bronx County', 36), (1339532, 59, 'Nassau County', 36), (1320134, 99, 'Palm Beach County', 12), (1280122, 35, 'Cuyahoga County', 39), (1229226, 57, 'Hillsborough County', 12), (1223348, 3, 'Allegheny County', 42), (1202362, 125, 'Oakland County', 26), (1163414, 49, 'Franklin County', 39), (1152425, 53, 'Hennepin County', 27), (1145956, 95, 'Orange County', 12), (1081726, 59, 'Fairfax County', 51), (1049025, 13, 'Contra Costa County', 6), (1029655, 35, 'Salt Lake County', 49), (1024266, 453, 'Travis County', 48), (998954, 189, 'St. Louis County', 29), (980263, 19, 'Pima County', 4), (971777, 31, 'Montgomery County', 24), (953207, 3, 'Honolulu County', 15), (949113, 119, 'Westchester County', 36), (947735, 79, 'Milwaukee County', 55), (930450, 19, 'Fresno County', 6), (927644, 157, 'Shelby County', 47), (920581, 121, 'Fulton County', 13), (919628, 119, 'Mecklenburg County', 37), (919040, 29, 'Erie County', 36), (916924, 43, 'DuPage County', 17), (916829, 1, 'Fairfield County', 9), (916542, 103, 'Pinellas County', 12), (905116, 3, 'Bergen County', 34), (903393, 97, 'Marion County', 18), (900993, 183, 'Wake County', 37), (894014, 3, 'Hartford County', 9), (864263, 31, 'Duval County', 12), (863420, 33, "Prince George's County", 24), (862477, 9, 'New Haven County', 9), (840978, 99, 'Macomb County', 26), (839631, 29, 'Kern County', 6), (823318, 111, 'Ventura County', 6), (809858, 23, 'Middlesex County', 34), (805321, 135, 'Gwinnett County', 13), (805235, 75, 'San Francisco County', 6), (805029, 5, 'Baltimore County', 24), (802374, 61, 'Hamilton County', 39), (800647, 141, 'El Paso County', 48), (799874, 91, 'Montgomery County', 42), (798552, 27, 'Worcester County', 25), (795225, 53, 'Pierce County', 53), (783969, 13, 'Essex County', 34), (782341, 85, 'Collin County', 48), (774769, 215, 'Hidalgo County', 48), (744344, 55, 'Monroe County', 36), (743159, 9, 'Essex County', 25), (741096, 111, 'Jefferson County', 21), (735334, 51, 'Multnomah County', 41), (722023, 25, 'Suffolk County', 25), (718633, 109, 'Oklahoma County', 40), (718451, 81, 'San Mateo County', 6), (713335, 61, 'Snohomish County', 53), (703462, 97, 'Lake County', 17), (691893, 89, 'DeKalb County', 13), (688078, 67, 'Cobb County', 13), (685306, 77, 'San Joaquin County', 6), (677560, 197, 'Will County', 17), (674158, 95, 'Jackson County', 29), (670850, 21, 'Norfolk County', 25), (662614, 121, 'Denton County', 48), (662564, 1, 'Bernalillo County', 35), (658466, 73, 'Jefferson County', 1), (634266, 17, 'Hudson County', 34), (630380, 25, 'Monmouth County', 34), (626681, 37, 'Davidson County', 47), (626667, 7, 'Providence County', 44), (625249, 17, 'Bucks County', 42), (622263, 41, 'El Paso County', 8), (620961, 510, 'Baltimore city', 24), (618754, 71, 'Lee County', 12), (603403, 143, 'Tulsa County', 40), (602622, 81, 'Kent County', 26), (602095, 105, 'Polk County', 12), (601723, 1, 'District of Columbia', 11), (600158, 31, 'Denver County', 8), (585375, 157, 'Fort Bend County', 48), (576567, 29, 'Ocean County', 34), (572003, 5, 'Arapahoe County', 8), (558979, 45, 'Delaware County', 42), (548285, 5, 'Bristol County', 25), (544179, 91, 'Johnson County', 20), (543376, 9, 'Brevard County', 12), (541781, 153, 'Summit County', 39), (538479, 3, 'New Castle County', 10), (537656, 3, 'Anne Arundel County', 24), (536499, 39, 'Union County', 34), (535153, 113, 'Montgomery County', 39), (534543, 59, 'Jefferson County', 8), (529710, 67, 'Washington County', 41), (519445, 71, 'Lancaster County', 42), (517110, 55, 'Douglas County', 31), (516564, 49, 'Utah County', 49), (515269, 89, 'Kane County', 17), (514453, 99, 'Stanislaus County', 6), (513657, 7, 'Camden County', 34), (508640, 123, 'Ramsey County', 27), (501226, 31, 'Passaic County', 34)]
countyPop2020 = [(10014009, 37, 'Los Angeles County', 6), (5275541, 31, 'Cook County', 17), (4731145, 201, 'Harris County', 48), (4420568, 13, 'Maricopa County', 4), (3298634, 73, 'San Diego County', 6), (3186989, 59, 'Orange County', 6), (2736074, 47, 'Kings County', 36), (2701767, 86, 'Miami-Dade County', 12), (2613539, 113, 'Dallas County', 48), (2418185, 65, 'Riverside County', 6), (2405464, 81, 'Queens County', 36), (2269675, 33, 'King County', 53), (2265461, 3, 'Clark County', 32), (2181654, 71, 'San Bernardino County', 6), (2110640, 439, 'Tarrant County', 48), (2009324, 29, 'Bexar County', 48), (1944375, 11, 'Broward County', 12), (1936259, 85, 'Santa Clara County', 6), (1793561, 163, 'Wayne County', 26), (1694251, 61, 'New York County', 36), (1682353, 1, 'Alameda County', 6), (1632002, 17, 'Middlesex County', 25), (1603797, 101, 'Philadelphia County', 42), (1585055, 67, 'Sacramento County', 6), (1525920, 103, 'Suffolk County', 36), (1492191, 99, 'Palm Beach County', 12), (1472654, 5, 'Bronx County', 36), (1459762, 57, 'Hillsborough County', 12), (1429908, 95, 'Orange County', 12), (1395774, 59, 'Nassau County', 36), (1323807, 49, 'Franklin County', 39), (1290188, 453, 'Travis County', 48), (1281565, 53, 'Hennepin County', 27), (1274395, 125, 'Oakland County', 26), (1264817, 35, 'Cuyahoga County', 39), (1250578, 3, 'Allegheny County', 42), (1185238, 35, 'Salt Lake County', 49), (1165927, 13, 'Contra Costa County', 6), (1150309, 59, 'Fairfax County', 51), (1129410, 183, 'Wake County', 37), (1115482, 119, 'Mecklenburg County', 37), (1066710, 121, 'Fulton County', 13), (1064465, 85, 'Collin County', 48), (1062061, 31, 'Montgomery County', 24), (1043433, 19, 'Pima County', 4), (1016508, 3, 'Honolulu County', 15), (1008654, 19, 'Fresno County', 6), (1004457, 119, 'Westchester County', 36), (1004125, 189, 'St. Louis County', 29), (995567, 31, 'Duval County', 12), (977203, 97, 'Marion County', 18), (967201, 33, "Prince George's County", 24), (959107, 103, 'Pinellas County', 12), (957419, 1, 'Fairfield County', 9), (957062, 135, 'Gwinnett County', 13), (955732, 3, 'Bergen County', 34), (954236, 29, 'Erie County', 36), (939489, 79, 'Milwaukee County', 55), (932877, 43, 'DuPage County', 17), (929744, 157, 'Shelby County', 47), (921130, 53, 'Pierce County', 53), (909235, 29, 'Kern County', 6), (906422, 121, 'Denton County', 48), (899498, 3, 'Hartford County', 9), (881217, 99, 'Macomb County', 26), (873965, 75, 'San Francisco County', 6), (870781, 215, 'Hidalgo County', 48), (865657, 141, 'El Paso County', 48), (864835, 9, 'New Haven County', 9), (863728, 13, 'Essex County', 34), (863162, 23, 'Middlesex County', 34), (862111, 27, 'Worcester County', 25), (856553, 91, 'Montgomery County', 42), (854535, 5, 'Baltimore County', 24), (843843, 111, 'Ventura County', 6), (830639, 61, 'Hamilton County', 39), (827957, 61, 'Snohomish County', 53), (822779, 157, 'Fort Bend County', 48), (815428, 51, 'Multnomah County', 41), (809829, 9, 'Essex County', 25), (797936, 25, 'Suffolk County', 25), (796292, 109, 'Oklahoma County', 40), (782969, 111, 'Jefferson County', 21), (779233, 77, 'San Joaquin County', 6), (766149, 67, 'Cobb County', 13), (764442, 81, 'San Mateo County', 6), (764382, 89, 'DeKalb County', 13), (760822, 71, 'Lee County', 12), (759443, 55, 'Monroe County', 36), (730395, 41, 'El Paso County', 8), (725981, 21, 'Norfolk County', 25), (725046, 105, 'Polk County', 12), (724854, 17, 'Hudson County', 34), (717204, 95, 'Jackson County', 29), (715884, 37, 'Davidson County', 47), (715522, 31, 'Denver County', 8), (714342, 97, 'Lake County', 17), (696355, 197, 'Will County', 17), (689545, 1, 'District of Columbia', 11), (676444, 1, 'Bernalillo County', 35), (674721, 73, 'Jefferson County', 1), (669279, 143, 'Tulsa County', 40), (660741, 7, 'Providence County', 44), (659399, 49, 'Utah County', 49), (657974, 81, 'Kent County', 26), (655070, 5, 'Arapahoe County', 8), (646538, 17, 'Bucks County', 42), (643615, 25, 'Monmouth County', 34), (637229, 29, 'Ocean County', 34), (620443, 339, 'Montgomery County', 48), (609863, 91, 'Johnson County', 20), (609017, 491, 'Williamson County', 48), (606612, 9, 'Brevard County', 12), (600372, 67, 'Washington County', 41), (588261, 3, 'Anne Arundel County', 24), (585708, 510, 'Baltimore city', 24), (584526, 55, 'Douglas County', 31), (582910, 59, 'Jefferson County', 8), (579200, 5, 'Bristol County', 25), (576830, 45, 'Delaware County', 42), (575345, 39, 'Union County', 34), (570719, 3, 'New Castle County', 10), (561891, 101, 'Pasco County', 12), (561504, 25, 'Dane County', 55), (553543, 127, 'Volusia County', 12), (552984, 71, 'Lancaster County', 42), (552878, 99, 'Stanislaus County', 6), (552352, 123, 'Ramsey County', 27), (541299, 81, 'Guilford County', 37), (540428, 153, 'Summit County', 39), (539339, 63, 'Spokane County', 53), (537309, 113, 'Montgomery County', 39), (534413, 29, 'Chester County', 42), (530819, 23, 'Plymouth County', 25), (525534, 45, 'Greenville County', 45), (524118, 31, 'Passaic County', 34), (523824, 173, 'Sedgwick County', 20), (523485, 7, 'Camden County', 34), (519572, 1, 'Adams County', 8), (516522, 89, 'Kane County', 17), (509285, 27, 'Morris County', 34), (503311, 11, 'Clark County', 53)]


#get the states
response = requests.get("https://api.census.gov/data/2010/dec/sf1?get=NAME&for=state:*")

states = re.split(",?\\n",response.text)
#skip the title
states = states[1:]

stateDict = {}

for i in states:
    matches = re.findall("\"(.*?)\"",i)
    stateDict[int(matches[1])] = matches[0]


#countyPop = []
#for i in stateDict.keys():
#    response = requests.get("https://api.census.gov/data/2010/dec/sf1?get=P001001,NAME&for=county:*&in=state:{:02}".format(i))
#    counties = re.split(",?\\n",response.text)[1:]
#    for j in counties:
#        #get rid of the state name
#        matchStr = "\"(.*?)(?:,\s{})?\"".format(stateDict[i])
#        matches = re.findall(matchStr,j)
#        pop = int(matches[0])
#        if(pop > 500e3):
#            countyPop.append((pop, int(matches[3]), matches[1], i))
#print(sorted(countyPop, reverse=True))

#countyPop2020 = []
#for i in stateDict.keys():
#    response = requests.get("https://api.census.gov/data/2020/dec/pl?get=P1_001N,NAME&for=county:*&in=state:{:02}".format(i))
#    counties = re.split(",?\\n",response.text)[1:]
#    for j in counties:
#        #get rid of the state name
#        matchStr = "\"(.*?)(?:,\s{})?\"".format(stateDict[i])
#        matches = re.findall(matchStr,j)
#        pop = int(matches[0])
#        if(pop > 500e3):
#            countyPop2020.append((pop, int(matches[3]), matches[1], i))

#print(sorted(countyPop2020, reverse=True))

#consider the top 15 in 2010 size, 2020 size, and net growth
#ensure Duval is included
#use county and state pairs as keys to ID entries

#delete the word county and add the state abbreviation
def getName(county, stateNum):
    return re.match("(.*?) County", county)[1] + ", "+ abbrev[stateDict[stateNum]]


useDict = {}
county2020Dict = {}
county2010Dict = {}
growthList = []

#data is 2010 population, county #, county name, state #
useDict[(31, 12)] = 'Duval, FL'
for i in countyPop2010[:15]:
    useDict[(i[1], i[3])] = getName(i[2], i[3])

for i in countyPop2010:
    county2010Dict[(i[1], i[3])] = i[0]

#values don't matter
for i in countyPop2020[:15]:
    useDict[(i[1], i[3])] = getName(i[2], i[3])

for i in countyPop2020:
    key = (i[1], i[3])
    #skip counties that did not have 500k pop in 2010
    if key not in county2010Dict:
        continue
    county2020Dict[key] = i[0]
    growthList.append([county2020Dict[key] - county2010Dict[key], key, i[2], i[3]])

growthList = sorted(growthList, reverse=True)
for i in growthList[:15]:
    key = i[1]
    useDict[key] = getName(i[2], i[3])

#create list of names, 2010 and 2020 pop count for the plot 
ml = []

for i in useDict.keys():
    ml.append([county2020Dict[i], useDict[i], county2010Dict[i] ])

ml = sorted(ml)
pop2020, names, pop2010 = zip(*ml)
pop2020 = np.array(pop2020)/1e6
pop2010 = np.array(pop2010)/1e6

#plt.figure(figsize=(15,8))


ax2LowerBound = 8.8
ratio = 5.5/(10 - ax2LowerBound)
fig , (ax1, ax2) = plt.subplots(1,2,sharey=True, gridspec_kw={'width_ratios':[ratio,1]})
fig.suptitle("County Growth 2010 to 2020")

# plot the same data on both axes

color2010 = 'C5'
color2020 = 'C2'
ax2.barh(names, pop2020, color = color2020)
ax2.barh(names, pop2010, color = color2010)
ax1.barh(names, pop2020, color = color2020)
ax1.barh(names, pop2010, color = color2010) 

ax2.set_xlim(ax2LowerBound, 10.5)
ax1.set_xlim(0, 5.5)
ax1.set_xticks([1,2,3,4,5])
ax2.set_xticks([9,10])
ax2.tick_params(axis='y', left=False)
ax1.set_xlabel("Millions of People")

ax1.spines.right.set_visible(False)
ax2.spines.left.set_visible(False)

colors = {'2010 Population':color2010, '2020 Growth':color2020}
labels = list(colors.keys())
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
ax1.legend(handles, labels)

#ax.set_yticks(base)
#ax.set_yticklabels(ageStr)

ax1.grid(axis='x', linestyle=(0,(3,10)))
ax2.grid(axis='x', linestyle=(0,(3,10)))

d = 2
kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
              linestyle="none", color='k', mec='k', mew=1, clip_on=False)
ax1.plot([1, 1], [0, 1], transform=ax1.transAxes, **kwargs)
ax2.plot([0, 0], [0, 1], transform=ax2.transAxes, **kwargs)

ax = plt.gca()
fig= plt.gcf()
plt.tight_layout()
plt.subplots_adjust(wspace=0.05)
plt.show()


##print queries to check data
#for i in useDict.keys():
#    print(useDict[i])
#    print(county2010Dict[i])
#    print("https://api.census.gov/data/2010/dec/sf1?get=P001001,NAME&for=county:{:03}&in=state:{:02}".format(i[0],i[1]))
#    print(county2020Dict[i])
#    print("https://api.census.gov/data/2020/dec/pl?get=P1_001N,NAME&for=county:{:03}&in=state:{:02}".format(i[0],i[1]))

