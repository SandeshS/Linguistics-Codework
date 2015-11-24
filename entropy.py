from __future__ import division
import sys
import csv
import math

inputFile = file(sys.argv[1], 'r')
reader = csv.reader(inputFile, delimiter = ',')
header = reader.next()

dataStore = []
for row in reader:
	dataStore.append(row)

dType = [str,str, int]

for i in range(0, len(dataStore)):
    dataStore[i] = [t(x) for t,x in zip(dType, dataStore[i])]

scoreDict = {}

for i in range(0, len(dataStore)):
	if dataStore[i][0] in scoreDict:
		scoreDict[dataStore[i][0]].append(dataStore[i][-1])
	else:
		scoreDict[dataStore[i][0]] = [dataStore[i][-1]]	

#print dataStore
#print scoreDict

entropies = []
for key in scoreDict:
	ids = []
	ids.append(key)
	entropies.append(ids)

#print entropies

#need to calculate entropy for each id
for key in scoreDict:
	sum = 0
	totalNum = 0
	for val in scoreDict[key]:
		sum += val
		totalNum += 1
	average = float(sum/totalNum)
	if average>=1 and average <= 5:
		scoreDict[key].append('agree')
	elif average < 1 and average > -1:
		scoreDict[key].append('neutral')
	elif average >= -5 and average <= -1:
		scoreDict[key].append('disagree')

agreeBin = 0
disagreeBin = 0
neutralBin = 0
totalBin = 0

#from math import log


aEntropy = 0
dEntropy = 0
nEntropy = 0
for key in scoreDict:
	for val in scoreDict[key]:
		if val>=1 and val<=5:
			agreeBin += 1
			totalBin += 1
		elif val<=-1 and val>=-5:
			disagreeBin += 1
			totalBin += 1
		elif val==0:
			neutralBin += 1
			totalBin += 1

	if agreeBin > 0 and totalBin > 0:
		aEntropy = (float(agreeBin/totalBin)*math.log((agreeBin/totalBin), 2))
	if disagreeBin > 0:
		dEntropy = (float(disagreeBin/totalBin)*math.log((disagreeBin/totalBin), 2))
	if neutralBin > 0:
		nEntropy = (float(neutralBin/totalBin)*math.log((neutralBin/totalBin), 2))
	entropy = -(aEntropy + dEntropy + nEntropy)
	if entropy == -0.0:
		entropy = 0.0
	scoreDict[key].append(entropy)
	aEntropy = 0
	agreeBin = 0
	disagreeBin = 0
	neutralBin = 0
	totalBin = 0
	dEntropy = 0
	nEntropy = 0

#for key in scoreDict:
#	print key, scoreDict[key]

minEntropy = 0.0
maxEntropy = 0.0

for key in scoreDict:
	if scoreDict[key][-1] < minEntropy:
		minEntropy = scoreDict[key][-1]
	if scoreDict[key][-1] > maxEntropy:
		maxEntropy = scoreDict[key][-1]

print 'For the Entire Dataset'
print 'Minimum Entropy\tMaximum Entropy'
print str(minEntropy) + '\t        ' + str(maxEntropy)

numMins = 0
numMax = 0
minsInAgree = 0
minsInDisagree = 0
minsInNeutral = 0
maxInAgree = 0
maxInDisagree = 0
maxInNeutral = 0

for key in scoreDict:
	if scoreDict[key][-1] == minEntropy:
		numMins += 1
		if scoreDict[key][-2] == 'agree':
			minsInAgree += 1
		elif scoreDict[key][-2] == 'neutral':
			minsInNeutral += 1
		elif scoreDict[key][-2] == 'disagree':
			minsInDisagree += 1
	elif scoreDict[key][-1] == maxEntropy:
		numMax += 1
		if scoreDict[key][-2] == 'agree':
			maxInAgree += 1
		elif scoreDict[key][-2] == 'neutral':
			maxInNeutral += 1
		elif scoreDict[key][-2] == 'disagree':
			maxInDisagree += 1

print 'Number of records with Minimum Entropies - ' + str(numMins)
print 'Number of records with Maximum Entropies - ' + str(numMax)
print '-----------------------------------------------------------------------------------------------------'
print '                           | Agree  |  Disagree  |  Neutral  |'
print 'Minimums                   |' + str(minsInAgree) + '      | ' + str(minsInDisagree) + '          | ' + str(minsInNeutral) + '        |'
print 'Maximums                   |' + str(maxInAgree) + '       | ' + str(maxInDisagree) + '         | ' + str(maxInNeutral) + '         |'
print '-----------------------------------------------------------------------------------------------------'
