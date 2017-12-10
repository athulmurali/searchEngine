from math import log

from inputs import *
from file_functions import *;
from Parser import *;
from Indexer import build_inverted_index


query =  	"hurricane isabel damage";


parsed_documents_path = os.path.join(master_path, parsed_docs_folder_name);
oneGram = 1 
inv_index			= build_inverted_index(parsed_documents_path,oneGram);
docLengthDict       = getDocumentLengthDict();







################################################

def calcdocLengthSum():
	sumAlldocLength = 0;
	for docId in docLengthDict:
		docLength = int (docLengthDict[docId])
		sumAlldocLength += docLength
	return sumAlldocLength;

def calcAvgDocLength():
	return calcdocLengthSum()/ len(docLengthDict)

def calcK(docID):
	dl = docLengthDict[docID];
	K = k1 * ((1 -  b) +  b * dl/avgDl);
	return K;


##################################################
# qfi  -  the term frequency in the query,
# As the relevance info is not given 
# the following should be zero 
ri 	= 0;
R 	= 0;

# Constants -----------------------------
k1	=1.2 
k2	=100
b 	=0.75

N 	=  len(docLengthDict) # number of documents containing the given term
avgDl = calcAvgDocLength()
print("N 			 	: "  , 	N);
print("Avg doc length 	: "  ,  avgDl);



# ****************************************************
# getDf: 
# dfDict - represents the dict containing 
           # {term1 : NumberOf DocumentsContainingIT,
           # {term2: NumberOf DocumentsContainingIT.. }

# term - String,
# 		the term for which the df has to be returned

# returns 0 if the given term is not in dfDict

# Tests success===============
# d = {"ap" : 13, "apple" : 100}

# print(getDf("ap"));  => 13
# print(getDf(ap0")); => 0

# ***************************************************
def getDf(term):
	# if the term is not present in any doc
	default  =0;

	if term in inv_index:
		
		tuplesList =inv_index[term];
		print("df  of term ",len(tuplesList))
		return len(tuplesList);
	else:
		return 0;
print("Find russian ------------------", getDf("russian"))
# *************************************************
# getTfInDoc():

# given : docId

# returns : 
# the number of term frequencies in a given doc
# ****************************************************
def getTfInDoc(term,docId):
	if term in inv_index:
		termTupleTuple = inv_index[term];
		for tup in termTupleTuple:
			if str(tup[0]) == str(docId):
				return tup[1];  
	
	# else the following return is executed
	return  0;

def getTopHits(rankedScoreList,n):
	return rankedScoreList[:n]

# *****************************************
# queryScoreDocument()
# The below function calculates  the score for a document 
# for the complete query
# ******************************************
def  queryScoreDocument(query,docId):
	termList = query.split(" ");
	# Doc score for the given query
	docScore = 0 
	for queryTerm in termList:
		# qfi  -  the term frequency in the query,
		qfi = query.count(queryTerm)
		ni  = getDf(queryTerm);
		print("qfi.,................",qfi)
		docScore += termScoreDocument(qfi,queryTerm, docId,ni);
	return docScore;


# The below function calculates  the score for a document 
# for  a given term from the query
def  termScoreDocument(qfi,term,docId,ni):
	print("term_score .... ",qfi,term,docId)

	K 	= calcK(docId);

	# ==========================================
	fi = getTfInDoc(term, docId)
	numerator =   ((ri + 0.5) /  (R - ri + 0.5))
	denominator =(ni - ri + 0.5)/(N - ni - R + ri + 0.5)

	logVal  =  log( numerator/ denominator )
	expr1 	=   (k1 + 1)*fi / (K + fi)
	expr2  	=  (k2 + 1)*qfi/ (k2 + qfi);

	docScore = logVal * expr1 * expr2;

	# print("Term :---------------   '", term);
	# print("logVal 		: ", logVal, \
	# 	"\nexpr1  		: ", expr1, \
	# 	"\nexpr2  		: ", expr2, \
	# 	"\nnumerator	: ", numerator,\
	# 	"\ndenominator	: ", denominator)
	# print("\nDoc score : ", docScore);

	return docScore;

# print(termScoreDocument(1,"is",0));

# Test**********************************************
# docId = 0
# query = "is name is";
# docSocreForQuery = queryScoreDocument("is name is",docId);
# print("Query 		: ",query,\
# 	"\ndoc_id  		: ",docId,\
# 	"\nDoc score 	: ",docSocreForQuery);



# scoreAllDocuments********************************
# returns : List of tuples like 
# [(1, 8.0),
# (2, 9.0)]
# where each tuple is (docId, score )
def scoreAllDocuments(query, docList):
	docScoreDict ={};
	for docId in docList:
		scoreListValues = [];
		print("query in doc :",query)
		score  =  queryScoreDocument(query, docId);
		docScoreDict[docId]  = score;
		# print(docId, "		: ",docScoreDict[docId]);	
	return docScoreDict;

# sortDocIdListByScore****************************
# returns : List of tuples like  (sorted from top scores to low scores)
# [  (2, 9.0),
#    (1, 8.0)]
# where each tuple is (docId, score )

def sortDocIdListByScore(docScoreDict):
	sortedDocScoreDict = sorted(docScoreDict.items(), \
	key=lambda k_v:  k_v[1], reverse=True)
	return sortedDocScoreDict;



# ================getSearchResults==============================
# queryList : represents the list of queries 
# each query in the list could be a single token or
# a string with multiple words

# n        : represents the number of top results to be returned 
# ==============================================================

# returns a list of doc id with their scores 
# Sorted  based on the document score in reverse 

# Example: 
# getSearchResults (hurricane isabel damage, 2)

#     docId :   Score
# => [{12 : 9.0},
    # {8  : 8.5}]



# getSearchResults***********************
# given :
# query -  String, the query for which the search must be performed
		# ex: "Hurricane", "Green Lights"
# hits  -  the number of results to be displayed 
# 			(top n : from high to low bm25 scores)

# returns 
# the top n docId:score tuples array 
# example : [(23,9.0), (12,8.0)]

def getSearchResults(query,hits = -1):
	# print("processing query :  ", query)
	scoredDocList 		=	scoreAllDocuments(query,getdocIdList());
	sortedDocScoreList 	=	sortDocIdListByScore(scoredDocList);
	if hits == -1 : len(sortedDocScoreList)
	topHitsList 		= 	getTopHits(sortedDocScoreList, hits);
	return topHitsList


# return dict 
# for each query in queryList
	# with query from queryList as key
	# results : List of tuples as valu
def searchListOfQueries(queryList, hits = -1):
	queryResults = {};

	for query in queryList:
		print("Query : ", query)
		queryResults[query] = getSearchResults(query,hits);
	return queryResults;

def topHitsDictToString(topHitsDict,hideScores = False):
	newStr = ""
	for searchQuery in topHitsDict:
		
		newStr = newStr + "\n" + str(searchQuery) + "--------------\n"
		for docScoreTuple in topHitsDict[searchQuery]:
			if hideScores == True:
				newStr = newStr + "   " + str(docScoreTuple[0])
			else :
				newStr = newStr + "\n" + str(docScoreTuple)
	return newStr

def writeTopHitsDictToTxt(fileName,topHitsDict, hideScores = False):
	with open(fileName, 'w') as file:
		file.write(topHitsDictToString(topHitsDict, hideScores) );
	return;



list_of_queries = ["russian "]
# topHitsDict = searchListOfQueries(listOfQueries,100);
topHitsDict = searchListOfQueries(list_of_queries);

print(topHitsDictToString(topHitsDict, hideScores = False));


writeTopHitsDictToTxt(bm25ResultsFile, topHitsDict,hideScores = True )
writeTopHitsDictToTxt(bm25ScoredResultsFile, topHitsDict,hideScores = False )