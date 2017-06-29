import file_reader
import rocchio_classifier
import query
import sys
import os

def svm_light_format(full_set):
    with open("./svm_light_format.txt", 'w') as output:
        for key in full_set:
            index = 1
            output.write(full_set[key][-1] + ' ')
            for feature in range(len(full_set[key])-1):
                if full_set[key][feature] != 0:
                    output.write(str(index) + ':' + str(full_set[key][feature]) + ' ')
                index += 1
            output.write('#' + key + '\n')


def calc_accuracy(test_set, classifier):
    correct = 0.0
    total = len(test_set.keys())
    for key in test_set:
        real = test_set[key][-1]
        predicted = classifier.predict(test_set[key][0:-1])
        print(real, predicted)
        if real == predicted:
            correct += 1.0
    return correct/total


if __name__ == '__main__':
    lab = 'lab10'  # use either lab9 or lab10 to switch between the lab work
    retrieval = sys.argv[1]  # number of search results to retrieve
    s_term = sys.argv[2]  # search term (query)
    method = sys.argv[3]  # type of vectorization to use
    if len(sys.argv) < 3:
        method = 'boolean'
    # queryID = sys.argv[4]  # only when creating files from within python!
    file_name = "./dataset/amazon_cells_labelled_full.txt"
    if lab == 'lab9':
        file_reader = file_reader.File_Reader(file_name, method)
        file_reader.vector_type = method
        full_set = file_reader.build_set(file_name)
        train_set = file_reader.build_set("./dataset/amazon_cells_labelled_train.txt")
        test_set = file_reader.build_set("./dataset/amazon_cells_labelled_test.txt")
        classifier = rocchio_classifier.Rocchio_Classifier(train_set)
        print(calc_accuracy(test_set, classifier))
        svm_light_format(full_set)
    elif lab == 'lab10':
        working_file = './temp_query_file'
        with open(working_file, 'w') as newfile:  # build new file inclusive of the search term (query)
            with open(file_name, 'r') as read:
                for line in read:
                    newfile.write(line)
            newfile.write(s_term + '	$s_term')  # give unique identifying class to the search term in the full file
        file_reader = file_reader.File_Reader(working_file, method)  # vector the new file into a workable set
        file_reader.vector_type = method
        full_set = file_reader.build_set(working_file)
        line_dict = file_reader.indexed_line  # get dictionary for "doc#" -> doc content
        new_query = query.Query(int(retrieval), full_set)  # find nearest results
        # if method == "boolean":  # use to create files from within python (w/ argv[4]).
        #     methodID = 1
        # else:
        #     methodID = 2
        # if not os.path.exists('./query_outputs'):
        #     os.makedirs('./query_outputs')
        # output_file = "./query_outputs/Output_"+str(queryID)+"_"+str(methodID)+".txt"
        # with open(output_file, 'w') as output:
        #     for result in range(len(new_query.output)):
        #         output.write(str(new_query.output[result][0])+' - '+str(line_dict[new_query.output[result][0]])+' Score:'+str(new_query.output[result][1])+'\n')
        for result in range(len(new_query.output)):
            print new_query.output[result][0], '-', line_dict[new_query.output[result][0]], 'Score:', new_query.output[result][1]
        os.remove(working_file)  # remove working file, no longer needed
