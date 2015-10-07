import sys
import operator

inputFile = open(sys.argv[1], 'r')
numberOfWords = 0
Dict  = {}

def stripPunctuations(word):
	pList = ["\'",".", ",", ":", ";", "!", "?", "/", "\\", "@", "#", "$", "%", "&", "(", ")", "\"", "-"]
	modWord = ""
	for i in word:
		if not i in pList:
			modWord = modWord + i
	return modWord

for line in inputFile.readlines():
	line = line.split()
	for word in line:
		numberOfWords += 1
		word = stripPunctuations(word)
		if not word in Dict:
			Dict[word] = 1
		else:
			Dict[word] += 1

sorted_di = sorted(Dict.items(), key = operator.itemgetter(1), reverse = True)
#print sorted_di

dataFile = open('rankedfrequencies.csv', 'w')
labels = "Rank,Word,Frequency\n"
dataFile.writelines(labels)

for (index, freq) in enumerate(sorted_di):
	#print index+1, freq[0], freq[1]
	currentline = "" + str(index+1) + "," + freq[0] + "," + str(freq[1]) + "\n"
	dataFile.writelines(currentline)
