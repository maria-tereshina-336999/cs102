import math
import re
from collections import Counter

from sklearn.metrics import accuracy_score


class NaiveBayesClassifier:
    def __init__(self, alpha=1):
        self.word_count = Counter({})
        self.class_count = {}
        self.alpha = alpha

    def del_punct_and_spaces(self, string):
        new_string = re.sub(r"[^\w\s\d+]", "", string.lower()).strip()
        return [new_string][0].split()

    def fit(self, X, y):
        """Fit Naive Bayes classifier according to X, y."""
        self.class_count = dict.fromkeys(set(y), 0)
        d = 0
        for i in range(len(X)):
            msg, lable = X[i], y[i]
            msgs = self.del_punct_and_spaces(msg)
            for word in msgs:
                self.class_count[lable] += 1
                if word not in self.word_count:
                    d += 1
                    self.word_count[word] = Counter(dict.fromkeys(set(y), 0))
                self.word_count[word][lable] += 1
        for i in self.word_count:
            for j in self.word_count[i]:
                self.word_count[i][j] = (self.word_count[i][j] + self.alpha) / (
                    self.class_count[j] + self.alpha * d
                )

    def predict(self, X):
        """Perform classification on an array of test vectors X."""
        prediction = []
        for x in X:
            clean_x = self.del_punct_and_spaces(x)
            mx = float("-inf")
            predicted_class = 0
            for label in self.class_count:
                m = sum(
                    [
                        math.log(self.word_count[wrd][label]) if self.word_count[wrd] else 0
                        for wrd in clean_x
                    ]
                )
                if m > mx:
                    mx = m
                    predicted_class = label
            prediction.append(predicted_class)
        return prediction

    def score(self, X_test, y_test):
        """Returns the mean accuracy on the given test data and labels."""
        return accuracy_score(self.predict(X_test), y_test)
