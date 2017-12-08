import math

corpus_length = 0


def bm25(ind_list, query_id, qr_list, relevance, dlength, final_length, bm25_score, stopwords):
    global corpus_length
    corpus_length = final_length
    already_cal = []
    for word in qr_list:
        if word not in stopwords and word not in already_cal and word in ind_list:
            already_cal.append(word)
            qfi = getqfi( word, qr_list )
            if len( relevance ) == 0:
                ri = 0
                for i in range( 0, len( ind_list[word] ), 1 ):
                    bm25_score[ind_list[word][i][0]] += getbm25( ind_list[word][i][1], len( ind_list[word] ), dlength[ind_list[word][i][0]], qfi, 0, ri )
            else:
                ri = get_ri( relevance[str( query_id )], ind_list[word] )
                for i in range( 0, len( ind_list[word] ), 1 ):
                    bm25_score[ind_list[word][i][0]] += getbm25( ind_list[word][i][1], len( ind_list[word] ), dlength[ind_list[word][i][0]], qfi, len( relevance[str( query_id )] ), ri )

    return bm25_score


def get_ri(relevant_docs, docs_with_term):
    ri = 0
    for items in docs_with_term:
        if items[0] in relevant_docs:
            ri += 1
    return ri


def getqfi(term, queries):
    count = 0
    for words in queries:
        if term == words:
            count += 1
    return count


def getbm25(fi, ni, dl, qfi, r, ri):
    total_docs = 3204
    avg_doc_len = float(corpus_length) / total_docs
    k1 = 1.2
    b = 0.75
    k2 = 100
    num = float(ri + 0.5) / (r - ri + 0.5)
    den = float(ni - ri + 0.5) / (total_docs - ni - r + ri + 0.5)
    task1 = (math.log(float(num) / den))
    task2 = ((fi * (k1 + 1)) / (fi + (k1 * ((1 - b) + (b * (dl / avg_doc_len))))))
    task3 = ((qfi * (k2 + 1)) / (qfi + k2))
    result = task1 * task2 * task3
    return result
