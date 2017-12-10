
# coding: utf-8

# In[1]:

import math
import os


from math import log
from inputs import *
from file_functions import *;
from Parser import *;
from Indexer import build_inverted_index
from CommonUtils import *

from Summarisation import *




parsed_documents_path = os.path.join(master_path, parsed_docs_folder_name);
oneGram = 1 

docLengthDict       = getDocumentLengthDict();
# In[2]:

INPUT_DIRECTORY = ""
INPUT_FOLDER = parsed_documents_path
QUERY = query_file_path
SMOOTHED_MODEL_SCORE_LIST = smoothened_LM_file_name
LAMBDA = 0.35


# In[3]:

def generateInvertedIndex():
    invertedIndex = {}
    tokenDict = {}
    files = os.listdir(INPUT_FOLDER)
    for file in files:
        print(files)
        file_name = os.path.join(parsed_documents_path,file)
        contents = open(file_name,"r").read()
        words = contents.split()
        length = len(words)
        file = file[:-4]
        tokenDict[file] = length
        for i in range(length):
            word = words[i]
            if word not in invertedIndex.keys():
                docIDCount = {file : 1}
                invertedIndex[word] = docIDCount
            elif file in invertedIndex[word].keys():
                invertedIndex[word][file] += 1
            else:
                docIDCount = {file : 1}
                invertedIndex[word].update(docIDCount)
    return invertedIndex


# In[4]:

def calculateLength():
    fileLengths = {}
    files = os.listdir(INPUT_FOLDER)
    for file in files:
        file =os.path.join(INPUT_FOLDER, file)
        doc = open(file,'r').read()
        file = file[:-4]
        fileLengths[file] = len(doc.split())
    print("length :",fileLengths)
    return fileLengths
# get_doc_length

# In[5]:

def queries(fileName):
    f = open(fileName,'r')
    queryList = []
    for line in f:
        line=" ".join(line.split())
        line=line.strip() 
        if line[-1] == '\n':            # Remove new line character
            queryList.append(line[0:-1])
        elif line[-1] == ' ':           # Remove last space
            queryList.append(line[0:-1])
        else:
            queryList.append(line)

    queryProcessor(queryList)
    return queryList


# In[6]:

def queryProcessor(querySet):
    queryTerms = {}
    for query in querySet:
        queryTerms[query] = query.split(" ")      
    return queryTerms


# In[7]:

# write the final maximum results document to a file
def rankedDocsFinal(docWeights, qid, maximumResults):
    file = open(SMOOTHED_MODEL_SCORE_LIST, "a")
    sortedList = sorted(docWeights, key=docWeights.__getitem__)
    top = sortedList[-(maximumResults):]
    top.reverse()
    rank = 0
    for doc in top:
        rank += 1
        text= str(qid+1) + "   " + "Q0" + "   " + str(doc) + "   " + str(rank) + "   " + str(docWeights[doc]) + "   " + "SmoothedQueryLikelihood" +"\n"
        file.write(text)
    file.write("\n\n ---------------------------------------------------------------------------------------\n\n\n")


# In[8]:

#calculating Query Likelihood Score for each query term
def SQLScore(maximumResults, total_collection, index, querySet, uniqueDocuments, doclength):
    qid = -1
    i=0
    score_accumulator=0
    queryTerms = queryProcessor(querySet)
    for query in querySet:
        qid += 1
        docWeights = {}
        for document in uniqueDocuments:
            documentScore = 0
            for queryTerm in list(set(queryTerms[query])):
                 if queryTerm in index.keys():
                    if document in index[queryTerm]:
                        termWeight_doc = index[queryTerm][document]
                    else:
                        termWeight_doc = 0
                    modD=doclength[document]
                    termWeight_collection= sum(index[queryTerm].values())
                    queryFreq_by_modD= termWeight_doc/modD
                    collectionFreq_by_total_collection= termWeight_collection/total_collection
                    score = (((1-LAMBDA)*queryFreq_by_modD)+(LAMBDA*collectionFreq_by_total_collection))
                    score_accumulator+=math.log(score)
            docWeights[document] = score_accumulator
            score_accumulator=0
        rankedDocsFinal(docWeights, qid, maximumResults)


# In[9]:

# Main. The program starts from here
def main():
 
    inv_index           = build_inverted_index(parsed_documents_path,oneGram);
    print("length ....",len(inv_index))


    maximumResults = 100
    
    uniqueDocuments=[]
    uniqueDocuments = [file[:-4] for file in os.listdir(INPUT_FOLDER)] #unique_docs(index) # Set of Docs

    total_docs = len(uniqueDocuments)          # Size of Corpus
    print("total_docs ",total_docs)
    
    doclength = calculateLength()              # Size of each document in a Dictionary
    return
    querySet = queries(QUERY)                  # Set of Queries
    total_collection=sum(doclength.values())
    SQLScore(maximumResults, total_collection, index, querySet, uniqueDocuments, doclength)      # Function call which computes document score
main()

