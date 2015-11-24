import sys
import csv

#first I need to read the csv file. The top row is the  header. Can be deleted. The other rows have relevant data

####################################################################
#
#  Functions will be here
#
####################################################################

#this function calculates the prior probabilities for the 2 classes. Consider only agreement and disagreement caategories. Ignore neutral cases
def calculatePriors(data):
	totalRecords = 0
	posPrior = 0
	negPrior = 0
	for record in data:
		if(record[1] >= 1 and record[1] <= 5):
			posPrior += 1
			totalRecords += 1
		elif (record[1] >= -5 and record[1] <= -1):
			negPrior += 1
			totalRecords += 1
	#print posPrior, negPrior
	#print totalRecords
	posPrior = float(posPrior)/totalRecords
	negPrior = float(negPrior)/totalRecords
	return (posPrior, negPrior)

#This function gets the responses of all the records where the class is 'Agreement'
def retrievePositives(response):
	posresp = []
	for i in range(0, len(response)):
		if response[i][1] >= 1 and response[i][1] <= 5:
			posresp.append(response[i][3])
	return posresp
	
#This function gets the responses of all the  records where the class is 'Disagreement'
def retrieveNegatives(response):
	negresp = []
	for i in range(0, len(response)):
		if response[i][1] >= -5 and response[i][1] <= -1:
			negresp.append(response[i][3])
	return negresp

#This function removes punctuations from the responses
def removePunc(line):
	puncSet = ['.', ',', '@','#', '\'', '\"', '!', '$', '-', '/', ':', ';', '(', ')', '?', '%', '&', '*', '_', '=', '|', '}', '{']
	newString = ''
	for char in line:
		if char not in puncSet:
			newString += char
	return newString

#Stop words do not give a strong indication of class. Hence they are eliminated from the responses
def removeStopWords(line):
	stopWordSet = ['and', 'a', 'the', 'an']
	newLine = ''
	for word in line.split():
		if word not in stopWordSet:
			newLine += word + ' '
	return newLine

#This function gets the count of number of words present in the responses
def getWordCount(wordDict):
	count = 0
	for value in wordDict.values():
		count += value
	return count


####################################################################
#
#  The main program starts here
#
####################################################################

#first we read the training data
inputFileTraining = file(sys.argv[1], 'r')
reader = csv.reader(inputFileTraining, delimiter=',')
header = reader.next()
data = []
for row in reader:
	data.append(row)

#Changing the data type to appropriate type
dType = [str, float, str, str]

for i in range(0, len(data)):
	data[i] = [t(x) for t,x in zip(dType, data[i])]

#print data
priors = ()
priors = calculatePriors(data)

#Keep a track of Prior probabilites for the two classes
posPriors = priors[0]
negPriors = priors[1]

#Prior probability has been found. Now to take care of the remainder of the numerator
responses = []
for i in range(0, len(data)):
	responses.append(data[i][3])

#Separating out the data into positive and negative sets
posResponses = retrievePositives(data)
negResponses = retrieveNegatives(data)

#remving the punctuations, converting to lower case and removing stop words in both positive and negative responses
for i in range(0, len(posResponses)):
	posResponses[i] = removePunc(posResponses[i])
	posResponses[i] = posResponses[i].lower()
	posResponses[i] = removeStopWords(posResponses[i])

for j in range(0, len(negResponses)):
	negResponses[j] = removePunc(negResponses[j])
	negResponses[j] = negResponses[j].lower()
	negResponses[j] = removeStopWords(negResponses[j])


#now need to create dictionaries for both agreement and disagreement
agreeDict = {}
disagreeDict = {}


#Count the occurence of words in the response
for line in posResponses:
	for word in line.split():
		if word in agreeDict:
			agreeDict[word] += 1
		else:
			agreeDict[word] = 1


for line in negResponses:
	for word in line.split():
		if word in disagreeDict:
			disagreeDict[word] += 1
		else:
			disagreeDict[word] = 1


#need to store probabilites in the dict

#need to get total of all words and total vocabulary size for entire dataset
posWordCount = getWordCount(agreeDict)
negWordCount = getWordCount(disagreeDict)

#This code just combines two dicts and checks the number of unique words
vocabularyCount = len(dict(agreeDict.items() + disagreeDict.items()))

#to incorporate unknown word - increase vocabulary by 1. This is constant throughout the program. This and posWordCount, negWordCount remains same
vocabularyCount += 1

#need to remove punctuations and common stop words from responses
#cleanResponses(responses)
#store all responses 

###############################################################
#
#  Handle testing data
###############################################################

inputFileTest = file(sys.argv[2], 'r')
readerTest = csv.reader(inputFileTest, delimiter=',')
#remove header
header2 = readerTest.next()
data2 = []
for row in readerTest:
	data2.append(row)


for i in range(0, len(data2)):
	data2[i] = [t(x) for t,x in zip(dType, data2[i])]

#need to retrieve only first three words of response - Store the responses from the test data 
testResponse = []
for i in range(0, len(data2)):
	testResponse.append(data2[i][3])

#convert everything to lower case
for i in range(0, len(testResponse)):
	testResponse[i] = testResponse[i].lower()
	testResponse[i] = removePunc(testResponse[i])
	testResponse[i] = removeStopWords(testResponse[i])

#remove punctuations and stop words

#now, we need to keep only 3 words of the response - better to keep all and check in dictionary for these words' probabilities

predictions = [] #0 for disagreement and 1 for agreement
aProb = 1.0
dProb = 1.0


#This part of code is using the Naive Bayes rules. It uses conditional probability and takes care of unknown words and laplace smoothing
for i in range(0, len(testResponse)):
	for word in testResponse[i].split():
		#first calculate agreement probability
		if word in agreeDict:
			aProb *= float(agreeDict[word] + 1)/ (posWordCount + vocabularyCount)
		else:
			#case for unknown word
			aProb *= 1/float(posWordCount + vocabularyCount)
	aProb *= posPriors
	for word in testResponse[i].split():
		if word in disagreeDict:
			dProb *= float(disagreeDict[word] + 1)/ (negWordCount + vocabularyCount)
		else:
			dProb *= 1/ float(negWordCount + vocabularyCount)
	dProb *= negPriors
	if(aProb > dProb):
		predictions.append(1)
	else:
		predictions.append(0)
	aProb = 1.0
	dProb = 1.0


#need to have final results in the form of rows separated by commas?
#for i in range(0, len(data2)):
#	print data2[i][1]

finalResults = []
finalResults.append(['id', 'actualClass', 'predictedClass'])

#need to first insert ids obtained for test data
for i in range(0, len(data2)):
	idl = []
	idl.append(data2[i][0])
	finalResults.append(idl)

#append actual class
for i in range(1, len(finalResults)):
	if data2[i-1][1] >= 1 and data2[i-1][1] <= 5:
		finalResults[i].append('agree')
	elif data2[i-1][1] >= -5 and data2[i-1][1] <= -1:
		finalResults[i].append('disagree')
	else:
		finalResults[i].append('neutral')

#misses out the last id
if data2[-1][1] >= 1 and data2[-1][1] <= 5:
	finalResults[-1].append('agree')
elif data2[-1][1] >= -5 and data2[-1][1] <= -1:
	finalResults[-1].append('disagree')
else:
	finalResults[-1].append('neutral')

#need to append predicted class
for i in range(0, len(predictions)):
	if predictions[i] == 1:
		finalResults[i+1].append('agree')
	elif predictions[i] == 0:
		finalResults[i+1].append('disagree')

consolidatedResults = []
for i in range(0, len(finalResults)):
	if finalResults[i][1] != 'neutral':
		consolidatedResults.append(finalResults[i])

#print finalResults[3]

dTypeforRes = [str, str, str]


for i in range(1, len(consolidatedResults)):
	consolidatedResults[i] = [t(x) for t,x in zip(dTypeforRes, consolidatedResults[i])]

#print consolidatedResults

#creating a confusion matrix and calculating evaluation metrics
from sklearn.metrics import confusion_matrix

Actual = []
Predicted = []
for i in range(1, len(consolidatedResults)):
	Actual.append(consolidatedResults[i][1])
	Predicted.append(consolidatedResults[i][2])

#print Actual, Predicted
resArray = confusion_matrix(Actual, Predicted)
truePositives = resArray[0][0]
trueNegatives = resArray[1][1]
falsePositives = resArray[1][0]
falseNegatives = resArray[0][1]

print '---------------------------------------------------------------------------------------'
print '|Predicted Class ->           Agree       Disagree                          '
print '|Actual Class |  Agree    \t' + str(truePositives) + ' \t  ' + str(falsePositives) + '      '
print '|                Disagree       ' + str(falseNegatives) + ' \t ' + str(trueNegatives) + '     '
print '----------------------------------------------------------------------------------------'
print 'Accuracy is - ' + str(float(truePositives+trueNegatives)/(truePositives + trueNegatives + falsePositives + falseNegatives))

print 'Precision for Agreement category - ' + str(float(truePositives)/(truePositives + falsePositives))
print 'Recall for Agreement category - ' + str(float(truePositives)/(truePositives + falseNegatives))

print 'Precision for Disagreement category - ' + str(float(trueNegatives)/(trueNegatives + falseNegatives))
print 'Recall for Disagreement category - ' + str(float(trueNegatives)/(trueNegatives + falsePositives))
