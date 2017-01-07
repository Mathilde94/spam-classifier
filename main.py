"""
This file will call the Naive Bayes Classifier and train and test data
"""

from classifier.model import NaiveBayesClassifier
from datastore.models import EmailsDataStore

nbc = NaiveBayesClassifier()

size_train, size_test = map(lambda x:int(x), raw_input("Specify your train and test data sizes:").split())


data_store = EmailsDataStore(max=10)
data_store.populate()
train_data = data_store.extract(count=size_train)

test_data = data_store.extract(start=size_train + 1, count=size_test)

nbc.prepare(train_data)
nbc.test(test_data)
