from nltk import ngrams


def get_high_tf(count, stop_words):
    unigrams = []
    tf = {}
    final = []
    for item in count:
        for each in ngrams((open("Corpus/" + str(item[0]), 'r').read()).split(), 1):
            unigrams.append(each[0])
    for item in unigrams:
        if item in tf:
            tf[item] += 1
        else:
            tf[item] = 1
    sorted_tf = sorted(tf.items(), key=lambda x : x[1], reverse=True)
    for each in sorted_tf:
        if each[0] not in stop_words:
            final.append(each[0])
    return final[:5]
