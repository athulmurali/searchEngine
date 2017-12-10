from bs4 import BeautifulSoup
import re
import traceback
import os
import glob

from inputs import *
import string


#Add functions below with your name in the function header
#Contains functions that can be used by all other modules
#For example, writeDictoJson, readFromFile,etc


# the following functino applies to CACM only. This has to be changed 
# Below the file name must be given withour location:
# For example
# if the actual file_name is 
# D:\\MS_Computer_Science\\IR\\Assignments\\Project\\searchEngine\\2017_11_8_16_31_29\\raw_documents\\CACM-3204.html'
# the file_name passed to the function must be CACM-3204.html
# file_path : 'CACM-' THe  prefix that is present in each and every file_name
# that is to be removed before creating a doc_id




#Function created by: Meghna
def transformation(data):

    pattern = r'\[.*?\]'
    data = data.strip();


    input = re.sub('\n+', " ", data)        
    input = re.sub(' +', " ", input)
    input= re.sub(r"(?<!\d)[.,;:](?!\d)"," ",input,0)
    input= re.sub(r"(?<![a-zA-Z\d])[-](?!\[a-zAa-Z\d)"," ",input,0)
    input=' '.join(word.strip(string.punctuation) for word in input.split())
    input= re.sub(r'\[.*?\]'," ",input)
    input= re.sub(r"([~|!/&$#'\"()\[\]=?\\])"," ",input,0)
    input = bytes(input, "UTF-8")    
    input = input.decode("ascii", "ignore")    
       
    return input.lower()



#Function created by: Meghna
def handle_punctuation(term):
    while term[:1] == "-" or term[:1] == "," or term[:1] == ".":
        if re.match(r'^[\-]?[0-9]*\.?[0-9]+$', term):
            return term
        if term[:1] == "-" or term[:1] == "." or term[:1] == ",":
            term = term[1:]
        else:
            return term
    return term

#returns a dict :
# key   : doc_id
# value : file_name of html doc with path
def createDocIDFileNameDict(html_files_directory_path):
    all_html_files_path = os.path.join(html_files_directory_path ,"*.html")
    all_files_in_dir  = glob.glob(all_html_files_path);
    doc_id_file_name_dict = {}
    for file_name in  all_files_in_dir:
        
        doc_id  = os.path.basename(file_name);
        doc_id = str.replace(doc_id,CACM_PREFIX,"")
        doc_id = doc_id.replace(".html","")
        doc_id_file_name_dict[str(doc_id)] =  str(file_name);
        # print(doc_id, str(file_name))
    return doc_id_file_name_dict;






def fileNameTodocID(file_name,file_path,extension):
    file_name.replace(file_path , "" )
    file_name.extension(extension, "")
    return file_name


def write_file(qid, query):
    if qid == 1:
        with open("Query.txt", 'w') as f:
            f.write(str(qid) + " " + query + "\n")
    else:
        with open("Query.txt", 'a') as f:
            f.write(str(qid) + " " + query + "\n")

#reads query from the file

def query_file_to_dict(query_file_name,stopping = False, stemming = False):
    
    query = {}
    count = 1
    query_text = open(query_file_name, 'r')
    q_soup = BeautifulSoup(query_text, 'html.parser')
    q_soup.prettify().encode('utf-8')
    for text in q_soup.findAll('docno'):
        text.extract()
    for text in q_soup.findAll('doc'):
        queries = text.get_text().strip(' \n\t')
        queries = str(queries)
        if stopping == True : 
            pass
        if stemming == True: 
            pass
        queries = queries.lower()
        queries = transformation(queries)
        write_file(count, queries)
        query[count] = queries.split(" ")
        count += 1
    return query


# returns a list of relevant_queries from query_relevance_doc

def relevant(query_rel_file_name):
    relevant = {}
    for line in open(query_rel_file_name, 'r'):
        words = line.split(" ")
        if words[0] in relevant:
            relevant[words[0]] += [words[2].replace(CACM_PREFIX,"") ]
        else:
            relevant[words[0]] = [words[2].replace(CACM_PREFIX,"") ]
    for i in range(1, 65):
        if str(i)in relevant:
            pass
        else:
            relevant[str(i)] = []
    return relevant

def getStopwordsList(file_name):
    stopwords = []
    for items in open(file_name, 'r').readlines():
        stopwords.append(items.strip("\n"))
    return stopwords


def stopping(str_words,stopwords):
    return ' '.join(filter(lambda x: x.lower() not in stopwords,  str_words.split()))

rel_dict = relevant(query_rel_file_name)
print(getStopwordsList(stop_list_file_name))



def get_query_rel_docs_dict():
    id_query_dict         = query_file_to_dict(query_file_path)
    query_doc_id_rel_dict = relevant(query_rel_file_name)

    query_rel_tuples =  ()
    for i in id_query_dict:
        query = " ".join(id_query_dict[i])
        # print("i",i, type(i))
        relevant_docs = query_doc_id_rel_dict[str(i)]
        # print(query, relevant_docs)
        # query_rel_dict[query]  = list(relevant_docs) ;
        new_tup = (i,query,list(relevant_docs))
        query_rel_tuples =  query_rel_tuples + (new_tup,);


    query_rel_tuples =sorted(query_rel_tuples, key=lambda tup: tup[0])

    return  query_rel_tuples;

# return the query list fromt the query file in order
def get_query_list():
    return [x[1] for x in get_query_rel_docs_dict()]

#returns a list of relevant documnet ids
def get_rel_doc_with_query(query):
    for queryTuple in  get_query_rel_docs_dict():
        if str(query) == queryTuple[1]:
            return queryTuple[2];
    return None


query_list = (get_query_list());
test_query = query_list[2];
print("Query to test : ",test_query)
print("Relevant docs for query: ",get_rel_doc_with_query(test_query))