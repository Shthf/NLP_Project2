import os
import re
import string

class Preprocessing:
    """
    This class is used to preprocess the files for use of Naive Bayes Classifier Class
    1. It removes all the punctuation from the text file
    2. It counts for each label and pass it as a dict
    3. It counts for each word in a file and pass it as a dict
    """
    
    ### go to the correct directory and for each file, remove the comma and lower the cases, save the unique words
    ### in vocab file
    def __init__(self, dir):   
        """Constructor
        Punctuation Removal Stage

        Args:
            dir (string): a string of directory path
        """
        
        self.dir = dir
        self.filepaths = []
        
        ## These two helper functions removes all punctuations other than ? and !
        def separate_punc(text):
            return re.sub(r"([^\s])([?!])", r"\1 \2 ", text)
        
        def remove_punc(text):
            valid_chars = string.ascii_letters + string.digits + "  ?!"  # Allowed characters (letters, digits, spaces, ?, !)
            return ''.join([char for char in text if char in valid_chars])

        
        
        # valid_chars = string.ascii_letters + string.digits + " !?-"
        
        for f in os.listdir(self.dir):
            if f == ".DS_Store": continue   # macOS Folder metadata
            for filename in os.listdir(self.dir + "/" + f):
                if filename.endswith(".txt"):
                    filepath = os.path.join(self.dir + "/" + f, filename)
                    self.filepaths.append(filepath)
                    
                    with open(filepath, 'r') as file:
                        text = file.read()
                    processed_text = separate_punc(remove_punc(text))
                        # lines = file.readlines()
                        
                        # modified_lines = []
                        # for line in lines:
                        #     modified_line = []
                        #     for char in line.strip():
                        #         if char.isalnum() or char.isspace(): 
                        #             modified_line.append(char)
                        #         else:
                        #             modified_line.append(" ")  
                        #             modified_line.append(char)  

                        #     modified_lines.append(''.join(modified_line)) 
                        
                    with open(filepath, "w") as file:
                        # file.writelines(modified_lines)
                        file.write(processed_text)
    
    
         
    
    def getPathList(self):
        """
        Returns:
            list: a list of paths
        """
        return self.filepaths
        
    def getLabels(self):
        """
        Returns:
            dict: a dict containing labels and count of each label
        """
        labels = dict()
       
        for f in os.listdir(self.dir):
            if f == ".DS_Store": continue
            for filename in os.listdir(self.dir + "/" + f):
                if filename.endswith(".txt"):
                    if f not in labels:
                        labels[f] = 1
                    else:
                        labels[f] += 1
        
        # print(labels)
        return labels
    
    
    # will only be used on training file
    # returns a dict of count of each word in a file
    def preTraining(self, label):
        """For a given path, it will count each word in each file and return the result

        Args:
            label (string): a string that indicates file name(the label)

        Returns:
            dict: a dict(label as the key) of dicts(containing the word count)
        """
        vector = dict()
        
        for filename in os.listdir(self.dir + "/" + label):
            if filename.endswith(".txt"):
                with open(self.dir + "/" + label + "/" + filename, 'r') as f:
                    for line in f:
                        words = line.split()

                        for word in words:
                            if word not in vector:
                                vector[word] = 1
                            else:
                                vector[word] += 1
                                
        return vector
    
    # will only be used on pretesting
    def preTesting(self, file):
        """For a given file, it returns the words that file contains as a list

        Args:
            file (string): a string of file path

        Returns:
            list: a list of words the file contains
        """
        words = []
        with open(file, 'r') as f:
            for line in f:
                words = line.split()
                
        return words
        
 