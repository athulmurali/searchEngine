from bs4 import BeautifulSoup
import corpus


def stopwords():
    stopwords_list = []
    for item in open('common_words', 'r').readlines():
        stopwords_list.append(item.strip("\n"))
    return stopwords_list


def relevant():
    relevant_data = {}
    for has_line in open("cacm.rel", 'r'):
        lines = has_line.split(" ")
        if lines[0] in relevant_data:
            relevant_data[lines[0]] += [lines[2] + ".txt"]
        else:
            relevant_data[lines[0]] = [lines[2] + ".txt"]

    for i in range(1, 65):
        if str(i)in relevant_data:
            pass
        else:
            relevant_data[str(i)] = []
    return relevant_data


def read_query():
    query = {}
    counter = 1
    query_text = open('cacm.query.txt', 'r')
    q_soup = BeautifulSoup(query_text, 'html.parser')
    q_soup.prettify().encode('utf-8')
    for text in q_soup.findAll('docno'):
        text.extract()
    for text in q_soup.findAll('doc'):
        qr = text.get_text().strip(' \n\t')
        qr = str(qr)
        qr = qr.lower()
        qr = corpus.transformation(qr)
        write_file(counter, qr)
        query[counter] = qr.split(" ")
        counter += 1
    return query


def write_file(query_id, queries):
    if query_id == 1:
        with open("query.txt", 'w') as f:
            f.write(str(query_id) + " " + queries + "\n")
    else:
        with open("query.txt", 'a') as f:
            f.write(str(query_id) + " " + queries + "\n")
