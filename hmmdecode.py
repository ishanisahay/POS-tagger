import sys
import json
import timeit
import codecs
from collections import Counter
from ast import literal_eval
from collections import MutableMapping
reload(sys)
sys.setdefaultencoding('utf8')

fw = codecs.open("hmmoutput.txt", 'w', 'utf-8')

def tagwithmaxprob(dictsOfTag):
	value = list(dictsOfTag.values())
	keys = list(dictsOfTag.keys())
	if bool(value):
		return keys[value.index(max(value))]

def func_viterbi_algo(transitionProb, emissionProb, wordStates, sentence):
	wordsPresent = sentence.split(" ")
	wordsLen = len(wordsPresent)
	prev = "START"

	states = []
	first_max_prob = {}
	startPtr = {}

	for tag in transitionProb:
		x = tag.split('->')
		states.append(x[0])
		states.append(x[1])
	

	uniqueStates = Counter(states).keys()
	prob_for_each_state = []
	backPtr = []

	#print wordsPresent
	statesToIter = []
	if wordsPresent[0].lower() in wordStates:
		statesToIter = wordStates[wordsPresent[0].lower()]
	else:
		statesToIter = uniqueStates

	for s in statesToIter:
		if s == "START":
			continue
		keyForEmission = wordsPresent[0]+'/'+s
		keyForTransition = prev + '->' + s

		if keyForEmission not in emissionProb:
			keyForEmission = "UNKNOWN" + '/' + s

		if keyForTransition in transitionProb and keyForEmission in emissionProb:
			first_max_prob[s] = emissionProb[keyForEmission] * transitionProb[keyForTransition]
			startPtr[s] = "START"
	
	bestState = tagwithmaxprob(first_max_prob)
	#print ("word: ", wordsPresent[0], "best tag sequence: ", bestState)

	prob_for_each_state.append(first_max_prob)
	backPtr.append(startPtr)


	for w in range(1, wordsLen):
		curr_max_prob = {}
		curr_ptr = {}
		preceding_prob = prob_for_each_state[-1]

		statesToIter = []
		if wordsPresent[w].lower() in wordStates:
			statesToIter = wordStates[wordsPresent[w].lower()]
		else:
			statesToIter = uniqueStates
			#print ("word not present",wordsPresent[w] )
		for s in statesToIter:
			if s == "START":
				continue
			if s == "END":
				continue
			bestPrevState = None
			best_prob = 0
			keyForEmissions = wordsPresent[w]+'/'+s
			if keyForEmissions not in emissionProb:
				#emissionProb[keyForEmissions] = 0
				#print ("key not in emission", keyForEmissions)
				keyForEmissions = "UNKNOWN" + '/' + s

			prevstatesToIter = []
			if wordsPresent[w-1].lower() in wordStates:
				prevstatesToIter = wordStates[wordsPresent[w-1].lower()]
			else:
				prevstatesToIter = uniqueStates

			for ps in prevstatesToIter:
				if ps == "END":
					continue
				keyForTransitionps = ps + '->' + s
				if keyForTransitionps not in transitionProb:
					transitionProb[keyForTransitionps] = 0
					#print ("state not in transition", keyForTransitionps)
				if ps not in preceding_prob:
					preceding_prob[ps] = 0
			
				
				probability = preceding_prob[ps] * transitionProb[keyForTransitionps] * emissionProb[keyForEmissions]
				if probability > best_prob:
					best_prob = probability
					bestPrevState = ps

			if bestPrevState == None: continue
			keyForTransitions = bestPrevState + '->' + s
			curr_max_prob[s] =  preceding_prob[bestPrevState] * transitionProb[keyForTransitions] * emissionProb[keyForEmissions]
			curr_ptr[s] = bestPrevState
			
		bestState = tagwithmaxprob(curr_max_prob)
		#print ("word: ", wordsPresent[w], "best tag sequence prev: ", bestState)
		prob_for_each_state.append(curr_max_prob)
		backPtr.append(curr_ptr)

	prev_path_end = prob_for_each_state[-1]
	prob = 0

	statesToIter = []
	if wordsPresent[wordsLen-1].lower() in wordStates:
		statesToIter = wordStates[wordsPresent[wordsLen-1].lower()]
	else:
		statesToIter = uniqueStates
	for s in statesToIter:
		if s not in prev_path_end:
			prev_path_end[s] = 0
		transKey = s + "->" + "END"
		#if transKey not in transitionProb:
			#transitionProb[transKey] = 0
		currProb = prev_path_end[s] * transitionProb[transKey]
		if currProb > prob:
			prob = currProb
			#lastPrevState = s
			bestState = s
			#print bestState

	
	finalState = ["END", bestState]
	backPtr.reverse()
	#print bestState
	##Backtrack
	curr_bestState = bestState
	for ptr in backPtr:
		finalState.append(ptr[curr_bestState])
		curr_bestState = ptr[curr_bestState]

	#final states appended in reverse order so reverse
	finalState.reverse()

	for i in range(0, wordsLen):
		fw.write(wordsPresent[i])
		fw.write('/')
		fw.write(finalState[i+1])
		fw.write(" ")
		if i == wordsLen:
			break

def main():

	start = timeit.default_timer()

	fp = codecs.open('hmmmodel.txt', "r", "utf-8")
	json_contents = fp.read()
	fp.close()
	data = json.loads(json_contents)
	wordStates = data["WORDSTATES"]
	transitionProb = data["TRANSPROB"]
	emissionProb = data["EMISSIONPROB"]
	
	fr = codecs.open(sys.argv[1], 'r', "utf-8")
	rawData = fr.read()
	lines = rawData.splitlines()

	cnt = 0;
	#test = "Up to 40 rockets had been fired at Israel , weeks after its military withdrew from the territory ."
	for each_sentence in lines:
		cnt += 1
		func_viterbi_algo(transitionProb, emissionProb, wordStates, each_sentence)
		fw.write("\n")
		#if cnt == 10:
			#break

	stop = timeit.default_timer()
	#print ("lines", cnt)
	#print stop - start 
	fw.close()

main()