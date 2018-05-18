# POS-tagger
A Hidden Markov Model part-of-speech tagger for English, Chinese, and Hindi. The training data provided is tokenized and tagged. The test data provided is tokenized, and the tagger adds the tags. 

# Training and test data
Two files (one English, one Chinese) with tagged training data in the word/TAG format, with words separated by spaces and each sentence on a new line. 
Two files (one English, one Chinese) with untagged development data, with words separated by spaces and each sentence on a new line.
Two files (one English, one Chinese) with tagged development data in the word/TAG format, with words separated by spaces and each sentence on a new line, to serve as an answer key.

# Programs
There are two programs: hmmlearn.py will learn a hidden Markov model from the training data, and hmmdecode.py will use the model to tag new data. The learning program will be invoked in the following way:

> python hmmlearn.py /path/to/input
ex:
> python hmmlearn.py en_train_tagged

The argument is a single file containing the training data; the program will learn a hidden Markov model, and write the model parameters to a file called hmmmodel.txt. The format of the model is up to you, but it should follow the following guidelines:

The model file should contain sufficient information for hmmdecode.py to successfully tag new data.

The tagging program will be invoked in the following way:

> python hmmdecode.py /path/to/input
ex:
> python hmmdecode.py en_dev_raw

The argument is a single file containing the test data; the program will read the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called hmmoutput.txt in the same format as the training data.

# Results
Results for English:
Correct: 22213
Total: 25096
Accuracy: 0.885121134842

Results for Chinese:
Correct: 10352
Total: 12012
Accuracy: 0.861804861805
