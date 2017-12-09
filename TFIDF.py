import queryfile
import math
import corpus
import indexer
import os

dlist = []
tfidf_count = {}
dlength = {}
ind_list = {}
qr_list = {}


def call_jobs():
    global tfidf_count, dlength, qr_list
    qr_list = queryfile.read_query()
    final_length = 0
    dlength = {}
    for item in ind_list:
        for one in ind_list[item]:
            final_length += one[1]
            if (one[0])in dlength:
                dlength[one[0]] += one[1]
            else:
                dlength[one[0]] = one[1]
    x = len(dlength)
    for query_id in qr_list:
        print("TFIDF Score", query_id)
        for each_document in dlist:
            tfidf_count[each_document] = 0.0
        tfidf_count = tfidf(ind_list, qr_list[query_id], x, dlength, tfidf_count, [])
        tfidf_score = sorted(tfidf_count.items(), key=lambda a : a[1], reverse=True)
        write_file(query_id, tfidf_score[:100], "TFIDF_Output", "tfidf")


def tfidf(index, query, n, doc_length, score, stopword):
    for word in query:
        if word not in stopword and word in index:
            ni = len(index[word])
            idf = math.log10(float(n) / ni)
            for item in index[word]:
                tf = float(item[1]) / doc_length[item[0]]
                if (item[0]) in score:
                    score[item[0]] += tf * idf
                else:
                    score[item[0]] = tf * idf
    return score


def write_file(query_id, val, name, alg_name):
    if not os.path.exists("Phase1"):
        os.makedirs("Phase1")
    ranking = 1
    for item in val:
        document = str(item[0])[:len(item[0])-4]
        if query_id == 1 and ranking == 1:
            with open("Phase1/" + name + ".txt", 'w') as f:
                f.write(str(query_id) + " Q0 " + document + " " + str(ranking) + " " + str(item[1]) + " " +
                        alg_name + "\n")
        else:
            with open("Phase1/" + name + ".txt", 'a') as f:
                f.write(str(query_id) + " Q0 " + document + " " + str(ranking) + " " + str(item[1]) + " " +
                        alg_name + "\n")
        ranking += 1


def main():
    global ind_list, dlist
    print("Corpus Generation")
    corpus.fetch_data()
    print("Indexer")
    ind_list = indexer.index_creation("corpus/")
    for one in ind_list:
        for item in ind_list[one]:
            if item[0] not in dlist:
                dlist.append(item[0])
    call_jobs()


def next_call():
    next_input = input("Do you wish to continue (y or n):\n")
    if next_input == "y" or next_input == "Y":
        call_jobs()


main()
