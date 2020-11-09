# FakeNewsClassifier

This project is to create a machine learning NLP model to predict Fake news on twitter.
Dataset consists of positive samples(real news) from CREDBANK data set and negative samples(fake news) from the Russian trolls.
I have used a pre-trained glove embedding ( reference: https://nlp.stanford.edu/projects/glove/ ) trained on a corpus from twitter with 100 dimensions.
LSTM model with an embedding layer of dimension 100, LSTM layer with 60 neurons, Global maxpooling, a hidden dense layer with 50 neurons and an ouput sense layer with 2 neurons is used.
Currently, the F1 score on test data is 0.77.
