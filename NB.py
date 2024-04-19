from Preprocessing import *

class NB:
    """Naive Bayes Classifier
    """
    def __init__(self, train_list, test_list):
        """Constructor

        Args:
            train_list (string): a string of file paths to be trained on
            test_list (string): a string of file paths to be tested on
        """
        self.prior_prob = dict()
        self.train_list = dict()
        # self.answer = dict()
        self.vocab = set()
        print("Start preprocess...")
    
    # get labels and update prior prob
    def getLabels(self):
        """Takes the label dict from preprocessing and calculate the prior probability of each
        """
        class_labels = pp_train.getLabels()
        # print(class_labels)
        total_label = sum(class_labels.values())
        
        for item in class_labels:
           class_labels[item] = class_labels[item] / total_label 

        # print("class_labels: ", class_labels)
        self.prior_prob = class_labels
        
        # with open(output, 'w') as o:
        #     o.write("Class labels: " + class_labels.toString() + "\n")
    
    def getVocab(self):
        """Get the vocab list from vocab file
        """
        with open(vocab, 'r') as f:
            for line in f:
                self.vocab.add(line.strip().split(' ')[0])

    def training(self):
        """Training process
           It will calculate probability of each word in the vocab for different labels with smoothing
           P(word|label) = (count(word, label) + 1)/count(total words + vocab size)
        """
        with open(output, 'a') as o:
            o.write("Now training...\n")
        
        vector_list = dict()
        self.getVocab()
        for label in self.prior_prob.keys():
            vector_list[label] = pp_train.preTraining(label)
        
        for item in vector_list.values():
            dic_sum = sum(item.values())
            
            for key in self.vocab:
                if key not in item: 
                    item[key] = 1/float(dic_sum + len(self.vocab))
                else:
                    item[key] = float(item[key] + 1)/float(dic_sum + len(self.vocab))
                    
        # print("After training, the assigned prob: ", vector_list)   
        with open(parameter, 'a') as p:
            for dic in vector_list:
                p.write("In " + dic + "\n")
                for key in vector_list[dic]:
                    p.write(key + ": " + str(vector_list[dic][key]) + "\n")
        
        self.train_list = vector_list
        # print(self.train_list["neg"]["mannage"])
        
        with open(output, 'a') as o:
            o.write("Training finished...\n")
      

    # given a file, predict the class and return the class and its probability
    def predict(self, file):
        """Prediction Process
        Multiply the prior probability and word probability to get the final probability
        of the sentence, and return the label that has the max prob

        Args:
            file (string): a string of file path to be predicted on

        Returns:
            string: a string of the label which is most likely to be true
        """
        words = pp_test.preTesting(file)    
        answer = dict()
        
        for prior_key in self.prior_prob.keys():
            # print(prior_key)
            prob = self.prior_prob[prior_key]
            for word in words:
                
                ## the word "mannage" is found in test folder but not in V, ignore it 
                if word not in self.train_list[prior_key]:
                    continue
                prob *= self.train_list[prior_key][word]
                
            
            answer[prior_key] = prob

        max_prob = max(answer.values())
        
        with open(output, 'a') as o:
            o.write("In file " + file + "\n")
            o.write("The probability to each class: ")
            for key in answer.keys():
                o.write(key + ": " + str(answer[key]) + " ")
            
            o.write("\nThe prediction is: " + next((key for key, val in answer.items() if val == max_prob), None) + "\n")
        # print("The prediction is: ", next((key for key, val in answer.items() if val == max_prob), None))
        return next((key for key, val in answer.items() if val == max_prob), None)

        
    def testing(self):
        """Testing Process
        This function will predict all the files in test directory and record the results
        into output.txt
        """
        # a dict that indicates how many files predicted correctly to each class/label
        prediction_dict = dict.fromkeys(self.prior_prob.keys(), 0)
        # a dict that indicates how many files have been tested so far
        sample_count = dict.fromkeys(self.prior_prob.keys(), 0)
        # a dict that indicates how many files are mispredicted in each class / label
        error_dict = dict.fromkeys(self.prior_prob.keys(), 0)
        
        for label in self.prior_prob:
            with open(output, 'a') as o:
                o.write("Now in testing\n")
                o.write("In class " + label + ": \n")
            for filename in os.listdir(test_folder + "/" + label):
                if filename.endswith(".txt"):
                    sample_count[label] += 1
                    
                    result_class = self.predict(test_folder + "/" + label + "/" + filename)
                    if  result_class == label:
                        prediction_dict[result_class] += 1
                    
                    with open(output, 'a') as o:
                        o.write("in label " + label + ": the count of correct match is " + str(prediction_dict[label]) + ", total is " + str(sample_count[label]) + "\n")
                    # print("in label ", label, ": the count of correct match is ", prediction_dict[label], "total is ", sample_count[label])
        
        # for pred_keys in prediction_dict.keys():
            error = abs(prediction_dict[label] - sample_count[label]) / sample_count[label]
            error_dict[label] = error
        
        with open(output, 'a') as o:
            o.write("The incorrectness is ")
            for key in error_dict.keys():
                 o.write(key + ":" + str(error_dict[key]) + " ")
            o.write("\n***************************************************************\n")
            
        # print("error_dict: ", error_dict)   
        print("Finished!")
        
    
        
# ## for toy data
# path = "./toy_data"
# train_folder = path + "/train"
# test_folder = path + "/test"
# vocab = path + "/toy_data.vocab"
# output = path + "/output.txt"
# parameter = path + "/parameter.txt"

### for real data
path = "./movie-review-HW2/aclImdb"
train_folder = path + "/train"
test_folder = path + "/test"
output = "./movie-review-HW2/output.txt"
vocab = path + "/imdb.vocab"
parameter = "./movie-review-HW2/parameter.txt"


pp_train = Preprocessing(train_folder)
train_path_list = pp_train.getPathList()
pp_test = Preprocessing(test_folder)
test_path_list = pp_test.getPathList()

nb = NB(train_path_list, test_path_list)
nb.getLabels()
nb.training()
nb.testing()
