import os, math
from optparse import OptionParser
import nltk
from nltk.stem import LancasterStemmer
from nltk.corpus import stopwords
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer


def vectorizer(string):
    tokens = nltk.tokenize.RegexpTokenizer(r'\w+').tokenize(string)
    result = []
    SW_set = stopwords.words('english')
    for word in tokens:
        checked = word.lower()
        if checked not in SW_set:
            stemming = LancasterStemmer()
            s_word = stemming.stem(checked)
            result.append(s_word)
    return result

def output_file_name(path):
    s = 's'
    l = 'l'
    t = 't'
    basedir = os.getcwd()
    if options.make_svmlight:
        l = 'L'
    if options.separate_folders:
        s = 'S'
        basedir = path
    if options.tfidf:
        t = 'T'
    prefix = os.path.basename(os.path.split(basedir)[0])+'_'+os.path.basename(basedir)
    return prefix+'_'+s+l+t+'.txt'


def output(folder_key):
    bag_of_words = {}
    index = 1
    f_key = folder_key

    for key in corpus.keys():
        currFolder = os.path.split(key)[0]
        if not options.separate_folders:
            f_key = currFolder
        if currFolder == f_key:
            for word in corpus[key]:
                if word not in bag_of_words.keys():
                    bag_of_words[word] = index
                    index += 1

    words_tf = {}
    words_wf = {}
    for key in corpus.keys():
        currFolder = os.path.split(key)[0]
        if not options.separate_folders:
            f_key = currFolder
        if currFolder == f_key:
            vec = len(bag_of_words) * [0, ]
            for word in corpus[key]:
                vec[bag_of_words[word]-1] += 1
            words_tf[key] = vec

    for key in corpus.keys():
        currFolder = os.path.split(key)[0]
        if not options.separate_folders:
            f_key = currFolder
        if currFolder == f_key:
            vec = len(bag_of_words.keys()) * [0, ]
            for word in corpus[key]:
                tempIndex = bag_of_words[word]-1
                if words_tf[key][tempIndex] > 0:
                    vec[tempIndex] = 1 + math.log(words_tf[key][tempIndex])
            words_wf[key] = vec
    df_vec = len(bag_of_words) * [0, ]
    workingDict = words_wf
    words_tfidf = {}

    if options.tfidf:
        for key in corpus.keys():
            currFolder = os.path.split(key)[0]
            if not options.separate_folders:
                f_key = currFolder
            if currFolder == f_key:
                for index in range(len(words_tf[key])):
                    if words_tf[key][index] > 0:
                        df_vec[index] += 1
        for key in corpus.keys():
            currFolder = os.path.split(key)[0]
            if not options.separate_folders:
                f_key = currFolder
            if currFolder == f_key:
                vec = len(bag_of_words.keys()) * [0.0, ]
                for word in words_tf[key]:
                    vec[word] = words_tf[key][word] * math.log(num_of_docs / df_vec[word])
                words_tfidf[key] = vec
        workingDict = words_tfidf
    file_classes = {}

    for key in corpus.keys():
        currFolder = os.path.split(key)[0]
        if not options.separate_folders:
            f_key = currFolder
        if currFolder == f_key:
            file_classes[key] = int(key[-5])

    output_file = './'+output_file_name(folder_key)
    with open(output_file, 'w'):
        string =

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-t", action="store_true", dest="tfidf")
    parser.add_option("-s", action="store_true", dest="separate_folders")
    parser.add_option("-l", action="store_true", dest="make_svmlight")
    (options, args) = parser.parse_args()

    corpus = {}
    folders = {}
    num_of_docs = 0

    for folder in args:
        folders[folder] = 1
        TEMP_RUN_LIMIT = 0  # TODO REMOVE FOR TESTING ONLY
        for filename in os.listdir(folder):
            f_key = folder+filename
            num_of_docs += 1
            if TEMP_RUN_LIMIT < 5:  # TODO REMOVE FOR TESTING ONLY
                filetext = ''
                with open(folder+'/'+filename, 'r') as reader:
                    for line in reader:
                        filetext += line[0:]
                corpus[f_key] = vectorizer(filetext)
                TEMP_RUN_LIMIT += 1  # TODO REMOVE FOR TESTING ONLY

    if options.separate_folders:
        for key in folders.keys():
            folder_key = key[0:-1]
            output(folder_key)
    else:
        output(os.getcwd())
