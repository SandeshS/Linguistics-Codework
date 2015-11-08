##################################
# I do not own this code.
# I have only edited parts of this code -
#	1. To read input from file
#
# Originally authored by - Prof. Marie-Catherine de Marneffe
#
##################################

import sys

datafile = sys.argv[1]


#sentence = ['people', 'with', 'rods', 'fish']
#n = len(sentence)

repr = ''
# initialize the chart
#chart = []
#for i in range(0,n):
#  row = []
#  for j in range(0,n):
#    row.append({})
#  chart.append(row)

#back = []
#for i in range(0,n):
#    row = []
#    for j in range(0,n):
#	row.append({})
#    back.append(row)

# build grammar
binaries = [
  [0.9, 'S', 'NP', 'VP'],
  [0.5, 'VP', 'V', 'NP'],
  [0.3, 'VP', 'V', '@VP_N'],
  [0.1, 'VP', 'V', 'PP'],
  [1.0, '@VP_N', 'NP', 'PP'],
  [0.1, 'NP', 'NP', 'NP'],
  [0.2, 'NP', 'NP', 'PP'],
  [1.0, 'PP', 'P', 'NP']
]
unaries = [
  [0.1, 'S', 'VP'],
  [0.7, 'NP', 'N'],
  [0.1, 'VP', 'V']
]

lexicon = [
  [0.5, 'N', 'people'],
  [0.2, 'N', 'fish'],
  [0.2, 'N', 'tanks'],
  [0.1, 'V', 'people'],
  [0.6, 'V', 'fish'],
  [0.3, 'V', 'tanks'],
  [0.1, 'N', 'rods'],
  [1.0, 'P', 'with']
]

def handleUnaries(i,j):
  modified = False
  for (p, A, B) in unaries:
    if chart[i][j].get(B,0)*p > chart[i][j].get(A, 0):
      #print str(chart[i][j].get(B,0)*p) + ' compared with ' + str(chart[i][j].get(A, 0))
      chart[i][j][A] = chart[i][j].get(B)*p
      #
      # store information necessary to backtrack
      #
      back[i][j][A] = (B, A)
      modified = True
  if modified:
    handleUnaries(i,j)

def tree2string(i, j, nonterm):
  # return string representation of tree with root <nonterm> in chart[i][j]
  # with the following format:
  # (<nonterm> <left-subtree> <right-subtree>)
  #    or
  # (<nonterm> <left-subtree> )
  #    or
  # (<nonterm> <term>)
  if (i == 0 and j == n-1):
	if back[i][j].get(nonterm, 0) == 0:
		print 'Sentence could not be constructed from the given grammar'
		return
  if not nonterm in sentence:
	print '(%s' % nonterm ,
  if i == j:
	temp = back[i][j].get(nonterm)
	print '(' + temp[0] ,
	while not temp[0] in sentence:
		temp = back[i][j].get(temp[0])
		print temp[0] ,
	print ')' ,
	return

  #repr = '(%s ' % nonterm
  root = back[i][j][nonterm]
  #print back[i][root[0]][root[1]]
  #print back[root[0]+1][j][root[2]]
  #print root
  #if root[-1] in sentence:
	#print reached
	#print root[-1]
  if(len(root) != 2): 
    left = tree2string(root[0], root[1]-1, root[3])
    right = tree2string(root[1], root[2]-1, root[4])

  print ')' ,
  #
  #  build current cell representation
  #

  #return repr

userInput = open(datafile, 'r').readlines()

for line in userInput:
	sentence = line.split()
	n = len(sentence)
	
	# initialize the chart
	chart = []
	for i in range(0,n):
	  row = []
	  for j in range(0,n):
	    row.append({})
	  chart.append(row)

	back = []
	for i in range(0,n):
	    row = []
	    for j in range(0,n):
		row.append({})
	    back.append(row)

	#The program starts here - First thing is filling up  the diagonal.      
	# lexicon
	for (i, word) in enumerate(sentence):
	  #print i, word
	  for (p, preterm, term) in lexicon:
	    if word == term:
	      #print word, term
	      chart[i][i][preterm] = p
	      #print chart[i][i], chart[i][i][preterm]
	      #
	      # store information necessary to backtrack
	      #
	      back[i][i][preterm] = (word, ')')     
	  handleUnaries(i,i)
	print 'words have been added on diagonal'


	#Need to analyze what this piece of code is doing
	# process all sets of #span words  
	for span in range(2,n+1):
	  #print ('span', span)
		for begin in range(0, n-span+1):
	    #print ('begin', begin)
			end = begin + span
			for split in range(begin+1,end):
	      #print('split', split)
	      # check all binary rules A -> B C
				for (p, A, B, C) in binaries:
					if chart[begin][split-1].get(B) and chart[split][end-1].get(C):
						prob = chart[begin][split-1].get(B)*chart[split][end-1].get(C)*p
						if prob > chart[begin][end-1].get(A,0):
							chart[begin][end-1][A] = prob
							back[begin][end-1][A] = (begin, split, end, B, C)
	            #
	            # store information necessary to backtrack
	            #
	    		handleUnaries(begin,end-1) 
	 
	
	print(chart[0][n-1])
	#print chart
	#print back[0] 
	#print back[1]
	#print back[2]
	#print back[3]
	tree2string(0,n-1,'S')
	print ''

def tree2string(i, j, nonterm):
  # return string representation of tree with root <nonterm> in chart[i][j]
  # with the following format:
  # (<nonterm> <left-subtree> <right-subtree>)
  #    or
  # (<nonterm> <left-subtree> )
  #    or
  # (<nonterm> <term>)
  if (i == 0 and j == n-1):
	if back[i][j].get(nonterm, 0) == 0:
		print 'Sentence could not be constructed from the given grammar'
		return
  if not nonterm in sentence:
	print '(%s' % nonterm ,
  if i == j:
	temp = back[i][j].get(nonterm)
	print '(' + temp[0] ,
	while not temp[0] in sentence:
		temp = back[i][j].get(temp[0])
		print temp[0] ,
	print ')' ,
	return

  #repr = '(%s ' % nonterm
  root = back[i][j][nonterm]
  #print back[i][root[0]][root[1]]
  #print back[root[0]+1][j][root[2]]
  #print root
  #if root[-1] in sentence:
	#print reached
	#print root[-1]
  if(len(root) != 2): 
    left = tree2string(root[0], root[1]-1, root[3])
    right = tree2string(root[1], root[2]-1, root[4])

  print ')' ,
  #
  #  build current cell representation
  #

  #return repr
  
    
#print(chart[0][n-1])
#print chart
#print back[0] 
#print back[1]
#print back[2]
#print back[3]
#tree2string(0,n-1,'S')
