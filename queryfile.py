from bs4 import BeautifulSoup
import corpus


def stopwords():
    stopwords_list = []
    for item in open('common_words', 'r').readlines():
        stopwords_list.append(item.strip("\n"))
    return stopwords_list


def read_query():
    queries = {}
    counter = 1
    q_text = open('cacm.query.txt', 'r')
    soup = BeautifulSoup(q_text, 'html.parser')
    soup.prettify().encode('utf-8')
    for content in soup.findAll('doc_num'):
        content.extract()
    for content in soup.findAll('doc'):
        query_list = content.get_text().strip(' \n\t')
        query_list = str(query_list)
        query_list = query_list.lower()
        query_list = corpus.transformation(query_list)
        queries[counter] = query_list.split(" ")
        counter += 1
    return queries


def write_file(query_id, queries):
    if query_id == 1:
        with open("query.txt", 'w') as f:
            f.write(str(query_id) + " " + queries + "\n")
    else:
        with open("query.txt", 'a') as f:
            f.write(str(query_id) + " " + queries + "\n")
