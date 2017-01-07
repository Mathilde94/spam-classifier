"""
This file will call the Naive Bayes Classifier and train and test data
"""

from classifier.model import NaiveBayesClassifier
from datastore.models import EmailsDataStore

nbc = NaiveBayesClassifier()

data_store = EmailsDataStore(max=10)
data_store.populate()
size_train = 210
train_data = data_store.extract(count=size_train)

test_data = data_store.extract(start=size_train + 1, count=30)

nbc.prepare(train_data)
nbc.test(test_data)
