import math
# from typing import Dict

class File_Reader:
    def __init__(self, input_file, vector_type='boolean'):
        self.file = input_file
        self.vector_type = vector_type
        self.words = {}  # type: Dict[str, int]
        self.stop_words = {}
        self.df = {}  # type: Dict[str, int]
        self.indexed_line = {}
        self.remove_stop_words()
        self.create_words_bank()
        if self.vector_type == 'boolean':
            self.build_set = self.build_set_boolean
        if self.vector_type == 'tf':
            self.build_set = self.build_set_tf
        if self.vector_type == 'tfidf':
            self.build_set = self.build_set_tfidf
    @property
    def vector_type(self):
        return self.vector_type

    @vector_type.setter
    def vector_type(self, value):
        if value in ('boolean', 'tf', 'tfidf'):
            self.vector_type = value

    def remove_stop_words(self):
        with open('./stop_words.txt', 'r') as stopwords:
            for line in stopwords:
                for word in line.split("\t")[0].split():
                    self.stop_words[self.string_cleanup(word)] = 1

    def string_cleanup(self, string):
        # return string
        # return string.lower()
        return string.lower().translate(None, "\",./][';<>|!@#$%^&=+*()|`-_~\\")

    def create_words_bank(self):
        index = 1 # starting with 1 because 0 cant serve as a dictionary key
        with open(self.file, 'r') as reader: # open the file "file"
            for line in reader: # for each line in file
                for word in line.split("\t")[0].split(): # for each word in the line
                    checked = self.string_cleanup(word)
                    if checked not in (self.words.keys() or self.stop_words.keys()):  # if the word doesnt already exist in the words dictionary
                            self.words[checked] = index  # add it
                            index += 1

    def count_file_lines(self, file_to_count):
        return sum(1 for line in open(file_to_count))

    def build_set_boolean(self, file_to_vector):
        doc_set = {}
        index = 0
        with open(file_to_vector, 'r') as reader:
            for line in reader:
                vec = len(self.words)*[0, ]
                for word in line.split("\t")[0].split():
                    checked = self.string_cleanup(word)
                    if checked not in self.stop_words.keys():
                        vec[self.words[checked]-1] = 1
                doc_class = line.split("\t")[1].rstrip()
                vec.append(doc_class)
                self.indexed_line['doc'+str(index)] = str(line.split("\t")[0:-1]).strip('[]"\'')
                doc_set['doc'+str(index)] = vec
                index += 1
        return doc_set

    def build_set_tf(self, file_to_vector):
        doc_set = {}
        index = 0
        with open(file_to_vector, 'r') as reader:
            for line in reader:
                vec = len(self.words)*[0, ]
                wf_vec = len(self.words)*[0, ]
                for word in line.split("\t")[0].split():
                    checked = self.string_cleanup(word)
                    if checked not in self.stop_words.keys():
                        vec[self.words[checked]-1] += 1
                for word in line.split("\t")[0].split():
                    checked = self.string_cleanup(word)
                    temp_index = self.words[checked]-1
                    if checked not in self.stop_words.keys():
                        if vec[temp_index] > 0:
                            wf_vec[temp_index] = 1 + math.log(vec[temp_index])
                doc_class = line.split("\t")[1].rstrip()
                wf_vec.append(doc_class)
                doc_set['doc'+str(index)] = wf_vec
                index += 1
        return doc_set

    def build_df(self, file_to_vector):
        df = {}
        with open(file_to_vector, 'r') as file:
            for line in file:
                wordlist = []
                for word in line.split("\t")[0].split():
                    checked = self.string_cleanup(word)
                    if checked not in self.stop_words.keys():
                        wordlist.append(checked)
                wordset = set(wordlist)
                for word in wordset:
                    if word in df.keys():
                        df[word] += 1
                    else:
                        df[word] = 1
        return df

    def build_set_tfidf(self, file_to_vector):
        tfidf_set = {}
        tf_set = self.build_set_tf(file_to_vector)
        idf = {}
        df = self.build_df(file_to_vector)
        n = self.count_file_lines(file_to_vector)
        for word in df.keys():
            idf[word] = math.log(n / df[word])
        with open(file_to_vector, 'r') as file:
            index = 0
            for line in file:
                doci = 'doc'+str(index)
                vec = len(self.words) * [0, ]
                for word in line.split("\t")[0].split():
                    checked = self.string_cleanup(word)
                    wordi = self.words[checked]-1
                    if checked not in self.stop_words.keys():
                        vec[wordi] = tf_set[doci][wordi] * idf[checked]
                doc_class = line.split("\t")[1].rstrip()
                vec.append(doc_class)
                self.indexed_line[doci] = str(line.split("\t")[0:-1]).strip('[]"\'')
                tfidf_set[doci] = vec
                index += 1
        return tfidf_set
