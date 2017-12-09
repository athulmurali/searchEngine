import corpus
import indexer
import queryfile
import BM25
import highTF
import os

ind_list = {}
qr_list = {}
dlist = []
tfidf_count = {}
bm25_score = {}
dlength = {}
stopwords = []


def call_jobs():
    global tfidf_count, dlength, qr_list, bm25_score, stopwords
    qr_list = queryfile.read_query()
    final_length = 0
    dlength = {}
    for item in ind_list:
        for one in ind_list[item]:
            final_length += one[1]
            if (one[0]) in dlength:
                dlength[one[0]] += one[1]
            else:
                dlength[one[0]] = one[1]
    x = len(dlength)
    print("Pseudo Relevance Feedback\n")
    for query_id in qr_list:
        print("BM25 score for query:", query_id)
        for each_document in dlist:
            bm25_score[each_document] = 0.0
        bm25_score = BM25.bm25(ind_list, query_id, qr_list[query_id], {}, dlength, final_length, bm25_score, [])
        sorted_bm25 = sorted(bm25_score.items(), key=lambda z: z[1], reverse=True)
        high_tf = highTF.get_high_tf(sorted_bm25[:10], stopwords)
        for each in high_tf:
            qr_list[query_id].append(each)
        for each_document in dlist:
            bm25_score[each_document] = 0.0
        bm25_score = BM25.bm25(ind_list, query_id, qr_list[query_id], {}, dlength, final_length, bm25_score, [])
        sorted_bm25 = sorted(bm25_score.items(), key=lambda z: z[1], reverse=True)
        write_file(query_id, sorted_bm25[:100], "PRF_BM25", "bm25")


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
    global ind_list, dlist, bm25_score, stopwords
    print("Corpus Generation")
    corpus.fetch_data()
    print("Indexer")
    ind_list = indexer.index_creation("corpus/")
    for one in ind_list:
        for item in ind_list[one]:
            if item[0] not in dlist:
                dlist.append(item[0])
    stopwords = queryfile.stopwords()
    call_jobs()


main()
