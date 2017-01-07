import math

from datastore.constants import NO_SPAM_TYPE, SPAM_TYPE

from .helpers import show_results


class NaiveBayesClassifier:

    N_NO_SPAM, N_SPAM = 0, 0
    K = 1

    def __init__(self):
        self.word_frequencies = {}
        self.words = {}

    def prepare(self, all_emails={}):
        self.get_words_frequencies(all_emails)
        self.N_SPAM = len(all_emails[SPAM_TYPE])
        self.N_NO_SPAM = len(all_emails[NO_SPAM_TYPE])
        self._get_spam_probabilities()

    def get_words_frequencies(self, all_emails):
        for type, emails in all_emails.items():
            for email in emails:
                email_words = email.extract_classifier_words()
                for w in email_words:
                    if w not in self.word_frequencies:
                        self.word_frequencies[w] = {NO_SPAM_TYPE: 0, SPAM_TYPE: 0}
                    self.word_frequencies[w][type] += 1

    def _get_spam_probabilities(self):
        for word, freq in self.word_frequencies.items():
            p_spam = float(freq[SPAM_TYPE] + 2 * self.K)/float(self.K + self.N_SPAM)
            p_no_spam = float(freq[NO_SPAM_TYPE] + 2 * self.K)/float(self.K + self.N_NO_SPAM)
            self.words[word] = (p_spam, p_no_spam)

    def test(self, test_data):
        tp, fp, tn, fn = 0, 0, 0, 0
        for type, emails in test_data.items():
            for email in emails:
                p_email_spam, p_email_no_spam = self._get_spam_probabilities_for_text(email)
                print(type, SPAM_TYPE if p_email_spam > p_email_no_spam else NO_SPAM_TYPE, email.subject)

                if type == SPAM_TYPE:
                    tp += int(p_email_spam > p_email_no_spam)
                    fn += 1 - int(p_email_spam > p_email_no_spam)
                else:
                    tn += int(p_email_no_spam > p_email_spam)
                    fp += 1 - int(p_email_no_spam > p_email_spam)

        show_results(tp, fp, fn, tn, len(test_data[SPAM_TYPE]), len(test_data[NO_SPAM_TYPE]))

    def _get_spam_probabilities_for_text(self, email):
        words = email.extract_classifier_words()
        p_spam = 0
        p_no_spam = 0
        for word, (p_w_spam, p_w_no_spam) in self.words.items():
            if word in words:
                p_spam += math.log(p_w_spam)
                p_no_spam += math.log(p_w_no_spam)
            else:
                p_spam += math.log(1-p_w_spam)
                p_no_spam += math.log(1-p_w_no_spam)

        # Getting back to the linear scale with math.exp:
        p_email_spam = math.exp(p_spam)
        p_email_no_spam = math.exp(p_no_spam)
        total = p_email_no_spam + p_email_spam
        p_email_spam = float(p_email_spam)/ float(total)
        p_email_no_spam = float(p_email_no_spam)/ float(total)

        return p_email_spam, p_email_no_spam
