A simple Naive Bayes Classifier has been used in order to classify emails as spam or not spam.

After retrieving the mbox files that contains the gmail emails, it will parse the emails and treat their subject titles.
 Currently a simple regex will try to retrieve some words (with punctuations). Lot of improvements can be done here.

It will then check the frequencies of those words for spam and no spam set of emails.

It can then run a test set of data and thanks to the Classifier, define them as spam or no spam.

The first and simple version of this classifier (with as well about 200 emails for the train data set) has a precision of 0.875 and recall of 0.7 with a f1 score  of 0.78.



