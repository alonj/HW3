import math
import sys


class Rocchio_Classifier:
    def __init__(self, train_set):
        self.training_set = train_set
        self.class_centroids = {}
        self.training()

    def training(self):
        for doc in self.training_set:
            doc_class = self.training_set[doc][-1]
            if doc_class not in self.class_centroids.keys():
                self.class_centroids[doc_class] = self.training_set[doc][0:-1]
            else:
                self.class_centroids[doc_class] = [self.class_centroids[doc_class][i] + self.training_set[doc][0:-1][i]
                                                   for i in range(len(self.training_set[doc]) - 1)]
        for c in self.class_centroids.keys():
            class_size = len(self.class_centroids[c])
            for i in range(class_size):
                self.class_centroids[c][i] /= float(class_size)
        print self.class_centroids.keys()

    def predict(self, doc_vec):
        minC = None
        minScore = sys.float_info.max  # for euclidean
        minScore = -1  # for cosine
        for c in self.class_centroids.keys():
            # currScore = self.euclidean_dist(self.class_centroids[c], doc_vec)  # for euclidean
            currScore = self.cosine_sim(self.class_centroids[c], doc_vec)  # for cosine
            # if currScore < minScore:  # for euclidean
            if currScore > minScore:  # for cosine
                minScore = currScore
                minC = c
        return minC

    @staticmethod
    def euclidean_dist(vec1, vec2):
        vecLen = len(vec1)
        sum = 0
        for i in range(vecLen):
            sum += (vec1[i] - vec2[i]) ** 2
        return sum ** 0.5

    @staticmethod
    def cosine_sim(vec1, vec2):
        vec_len = len(vec1)
        product_sum = 0
        l2norm_vec1 = 0
        l2norm_vec2 = 0
        for i in range(vec_len):
            product_sum += vec1[i] * vec2[i]
            l2norm_vec1 += vec1[i] ** 2
            l2norm_vec2 += vec2[i] ** 2
        l2norm_vec1 **= 0.5
        l2norm_vec2 **= 0.5
        return product_sum / (l2norm_vec1 * l2norm_vec2)
