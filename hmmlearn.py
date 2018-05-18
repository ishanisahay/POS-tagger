from collections import Counter
import json
import sys
import timeit
import codecs
reload(sys)
sys.setdefaultencoding('utf8')

start = timeit.default_timer()
fp = codecs.open(sys.argv[1], 'r', "utf-8")
lines = fp.read().splitlines()
fp.close()

fw = codecs.open('hmmmodel.txt', 'w', "utf-8")

obs_given_tag = []
state_trans = []
transferrable_state = []
for line in lines:
	sentence = line.split(" ")
	temp = []
	start_state = "START"
	temp.append(start_state)
	for tagged_word in sentence:
		obs_given_tag.append(tagged_word)
		s = tagged_word.rsplit('/', 1)
		temp.append(s[1])

	end_state = "END"
	temp.append(end_state)
	for i, j in zip(temp, temp[1:]):
		key_for_trans = i + "->" + j
		state_trans.append(key_for_trans)
		transferrable_state.append(i)

count_state_trans = Counter(state_trans)
#CHECK THIS, count should be states which can be transitioned
count_transferrable_State = Counter(transferrable_state)

#split key of state_trans to get the previous tag
transition_prob = {}
for item in state_trans:
	k = item.split("->")
	prev_tag_count = count_transferrable_State[k[0]]
	transition_count = count_state_trans[item]
	if (prev_tag_count != 0):
		transition_prob[item] = float(transition_count)/ float(prev_tag_count)

states = []
states.append("START")
word_possible_states = {}
for word in obs_given_tag:
	y = word.rsplit('/', 1)
	states.append(y[1])
	'''if y[0] in word_possible_states:
		if y[1] not in word_possible_states[y[0]]:
			word_possible_states[y[0]].append(y[1])
	else:
		word_possible_states[y[0]] = [y[1]]'''
	wordKey = y[0].lower()
	if wordKey in word_possible_states:
		if y[1] not in word_possible_states[wordKey]:
			word_possible_states[wordKey].append(y[1])
	else:
		word_possible_states[wordKey] = [y[1]]

states.append("END")
count_of_tags = Counter(states)
uniqueStates = Counter(count_of_tags).keys()
emission_obs_given_tag = {}
count_obs_tags = Counter(obs_given_tag)

vocab = word_possible_states.keys()
totalWords = len(vocab)

for key, value in count_obs_tags.iteritems():
	t = key.rsplit('/', 1)
	no_of_t = count_of_tags[t[1]]
	if (no_of_t != 0):
		emission_obs_given_tag[key] = float(value)/float(no_of_t)

for s in uniqueStates:
	if s == "START":
		continue
	if s == "END":
		continue
	key = "UNKNOWN" + '/' + s
	emission_obs_given_tag[key] = float(1) / float( count_of_tags[s] + totalWords)

for s1 in uniqueStates:
	for s2 in uniqueStates:
		keyForTrans = s1 + "->" + s2
		if keyForTrans not in transition_prob:
			transition_prob[keyForTrans] = float (1) / float(count_transferrable_State[s1] + totalWords)
		else:
			transition_prob[keyForTrans] = float (1+ count_state_trans[keyForTrans])/  float (count_transferrable_State[s1] + totalWords)


my_json_obj = json.dumps({'WORDSTATES': word_possible_states, 'TRANSPROB': transition_prob, 'EMISSIONPROB': emission_obs_given_tag })
fw.write(my_json_obj)
fw.close()
stop = timeit.default_timer()
#print stop - start 