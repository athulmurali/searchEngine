import math


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
