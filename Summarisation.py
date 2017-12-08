#Author : Athul Muralidharan

# The following constants must be moved to inputs.py
RELEVANT     = "R"
NON_RELEVANT = "N"

from functools import reduce


# format
# doc_relevance_table = {"1" : "R", "2" : "R", "3" : "N" , "4" : "R"}


#Dependencies:
# doc_relevance_table
# { doc_id : Relevance, doc_id : Relevance} from user


#takes in a string as parameter,
# returns true if the string is a string that represents relevance
# in case, multi state relevance, 

def isRelevant(relevance):
    return ( relevance == RELEVANT)


# returns the tuple if the tuple doc_id matches,
# else returns None
# print(getTupByDocID(  (("1","R"),("2","N")) , "1")) => ('1', 'R')
# print(getTupByDocID(  (("1","R"),("2","N")) , "5")) => None

def getTupByDocID(tuple_of_tuples,doc_id):
    for tup in tuple_of_tuples:
        if str(tup[0]) == str(doc_id):
            return tup
    return None


#returns the count of the documents that are relevant
def getRelevantDocCount(doc_id_tuples):
    count = 0;
    for doc_id_rel_tup in doc_id_tuples:
        if isRelevant(doc_id_rel_tup[1]):
            count +=1 

    return count;

    

class SummaryRecord:
    #data structure : dict
# {doc_id : (relevance, precision, recall)}
# doc_id  : String
# relevance : Char, To support multi state relevance instead of binary in the future
# precision : Float, 0.5 , 0.6 etc
# recall    : Float , 0.4, 0.5,etc
    # Constructor: Sets the field values
    def __init__(self, doc_id, relevance,precision, recall):
        self.doc_id     = doc_id
        self.relevance  = relevance
        self.precision  = precision
        self.recall     = recall

        # To print function for objects
    def __str__(self):
        return  "doc_id :  " +  str(self.doc_id) +\
        "\trelevance : " + str(self.relevance)+\
        "\tprecision : " + str(self.precision)+\
        "\t\trecall    : " + str(self.recall)

class SummaryTable:
    def buildSummaryTable(self,doc_relevance_table):
        relevant_doc_count = getRelevantDocCount(doc_relevance_table)
        temp_relevant_count = 0;
        temp_doc_count      = 0;
        summary_table = [];
        
        for doc_id_rel_tup in doc_relevance_table:
            temp_doc_count += 1
            if isRelevant(doc_id_rel_tup[1]):
                temp_relevant_count += 1

            doc_id =    doc_id_rel_tup[0]
            relevance = doc_id_rel_tup[1]
            precision = temp_relevant_count/temp_doc_count;
            recall    = temp_relevant_count/relevant_doc_count
            new_summary_record = SummaryRecord(doc_id,relevance,precision,recall)
            summary_table.append(new_summary_record)
        return summary_table;


    def __init__(self,doc_id_relevance_list):
        self.table =  self.buildSummaryTable(doc_id_relevance_list)

    def getSummaryTable(self):
        return self.table;


    def summaryTableToString(self):
        str_out = "k\t\t\tdoc_id\t\t\trelevance\t\t\tprecision\t\t\trecall"
        k =0;
        for summary_table_record in self.table:
            temp_record_str = "\n" + str(k)+ "\t\t"      +\
            "\t\t" + str(summary_table_record.doc_id)    +\
            "\t\t\t" + str(summary_table_record.relevance) +\
            "\t\t\t\t\t" + (str.format("{0:.3f}",summary_table_record.precision)) +\
            "\t\t\t\t" + str.format("{0:.3f}",summary_table_record.recall)+"\n"
            str_out = str_out + temp_record_str;
            k+=1;
        return str_out

    def getPrecision(self,doc_id):
        for summaryObj in self.table:
            if summaryObj.doc_id == doc_id:
                return summaryObj.precision;
# returns the precision value of the object at k in the table
#array index starts from 0
# but k value starts from 1 
    def getPrecisionAtK(self,k):
        if (0<= k <=  len(self.table)):
            return self.table[k-1].precision;
        else: return None;

# returns Average Precision
    def calcAP(self):
        sum_of_precisions = reduce (lambda a,b : a + b.precision, self.table,0) 
        number_of_documents = len(self.table)
        return   sum_of_precisions * 1.0/number_of_documents 

# returns the i  at which the first relevant document is found
# if no relevant documents are present; returns None
# getKofFirstRelevantDoc
    def calcRR(self):
        for i in range(len(self.table)):
            if (  isRelevant(self.table[i].relevance )):
                return  1.0/(i+1);
        return None;


#Tasks:
# 1.MAP
def calcMAP(queries_results_tuples ):
    AP_list = []
    for query_result_tuple in queries_results_tuples:
        # query_result_tuple[1] returns a tuple of tuples ofdoc_id,relevance
        print("query_result_tuple", query_result_tuple)
        temp_summary_table = SummaryTable(query_result_tuple[1]);
        AP_list.append(temp_summary_table.calcAP())
    sum_of_AP           =  sum(AP_list)
    number_of_AP        =  len(AP_list)

    return   sum_of_AP * 1.0/number_of_AP 

# returns : a float
def calcMRR(queries_results_tuples):
    RR_list = []
    for query_result_tuple in queries_results_tuples:
        # query_result_tuple[1] returns a tuple of tuples ofdoc_id,relevance
        temp_summary_table = SummaryTable(query_result_tuple[1]);
        RR_list.append(temp_summary_table.calcRR());

    sum_of_RR           =  sum(RR_list)
    number_of_RR        =  len(RR_list)

    return   sum_of_RR * 1.0/number_of_RR 


# returns: list [list of integers]
# each list in this list represents a precision list for a query
# the list is returned in the same order as same the queries given
def pAtK(queries_results_tuples,k_list):
    p_at_k_list = []
    for query_result_tuple in queries_results_tuples:
        # query_result_tuple[1] returns a tuple of tuples ofdoc_id,relevance
        temp_summary_table = SummaryTable(query_result_tuple[1]);
        p_list_current_query = []
        for k in k_list:
            p_list_current_query.append(temp_summary_table.getPrecisionAtK(int(k)));
        p_at_k_list.append(p_list_current_query)
    return   p_at_k_list;

def printAllTables(queries_results_tuples):
    for query_result_tuple in queries_results_tuples:
        temp_summary_table = SummaryTable(query_result_tuple[1]);
        print("Query : ", query_result_tuple[0])
        print(temp_summary_table.summaryTableToString())
        


# QueryResults =  \
# ("query1", ((1,"R"), (2,"N") ),\
# ("query2", ((1,"N"), (2,"R") ))

# #tuple from the array of tuples
# for queryResult in queryResultsTuples: 
    # current tuple contains (queryString, Tuple of Tuples((doc_id1,Relevance),(doc))



# Testing and execution
# {"1" : "N", "2" : "R", "3" : "N" , "4" : "R"} old fomat in dict
query_results = (("1","N"),("2","R"),("3","N"),("4","R"))
query_results2 = (("1","N"),("2","N"),("3","N"),("4","R"))

print("Given  query results:  ",query_results)
summary_table = SummaryTable(query_results)


for i in summary_table.getSummaryTable() : print(i);
print("P@K : ",summary_table.getPrecisionAtK(3))
print("AP  : ",summary_table.calcAP())
print("RR  : ",summary_table.calcRR())


# Task3 Delivarables  : Output============================
queries_results_tuples = (("query1", query_results), ("query2" ,query_results2))

print("*******************Summarisation tables*******************");
printAllTables(queries_results_tuples);
# print("queries_results_tuples :",queries_results_tuples)
print("MAP :", calcMAP(queries_results_tuples))
print("MRR :", calcMRR(queries_results_tuples))

get_precision_at_list = [1,2,3]
print("P@K :", pAtK   (queries_results_tuples, get_precision_at_list))