from bs4 import BeautifulSoup
import re



def stopwords():
    stopwords = []
    for items in open('common_words', 'r').readlines():
        stopwords.append(items.strip("\n"))
    return stopwords


def relevant():
    relevant = {}
    for line in open("cacm.rel", 'r'):
        lines = line.split(" ")
        if lines[0] in relevant:
            relevant[lines[0]] += [lines[2] + ".txt"]
        else:
            relevant[lines[0]] = [lines[2] + ".txt"]
    for i in range(1, 65):
        if str(i)in relevant:
            pass
        else:
            relevant[str(i)] = []
    print(relevant)
    return relevant


def read_query():
    query = {}
    count = 1
    query_text = open('cacm.query.txt', 'r')
    q_soup = BeautifulSoup(query_text, 'html.parser')
    q_soup.prettify().encode('utf-8')
    for text in q_soup.findAll('docno'):
        text.extract()
    for text in q_soup.findAll('doc'):
        queries = text.get_text().strip(' \n\t')
        queries = str(queries)
        queries = queries.lower()
        queries = transformation(queries)
        write_file(count, queries)
        query[count] = queries.split(" ")
        count += 1
    return query


def transformation(data):
    data = re.sub(r'[@_!\s^&*?#=+$~%:;\\/|<>(){}[\]"\']', ' ', data)
    term_list = []
    for term in data.split():
        term_len = len(term)
        if term[term_len - 1:term_len] == '-' \
                or term[term_len - 1:term_len] == ',' \
                or term[term_len - 1:term_len] == '.':
            term = term[:term_len - 1]
            term_list.append(handle_punctuation(term))
        else:
            term_list.append(handle_punctuation(term))
    term_list = [x for x in term_list if x != '']
    term_list = " ".join(term_list)
    if ' PM ' in term_list or 'PM ' in term_list or 'PMB ' in term_list:
        term_list_proc = term_list.split('PM')[0]
        term_list_proc += " pm"
        return term_list_proc
    elif ' AM ' in term_list or 'AM ' in term_list:
        term_list_proc = term_list.split('AM')[0]
        term_list_proc += " am"
        return term_list_proc
    else:
        return term_list


def handle_punctuation(term):
    while term[:1] == "-" or term[:1] == "," or term[:1] == ".":
        if re.match(r'^[\-]?[0-9]*\.?[0-9]+$', term):
            return term
        if term[:1] == "-" or term[:1] == "." or term[:1] == ",":
            term = term[1:]
        else:
            return term
    return term


def write_file(qid, query):
    if qid == 1:
        with open("Query.txt", 'w') as f:
            f.write(str(qid) + " " + query + "\n")
    else:
        with open("Query.txt", 'a') as f:
            f.write(str(qid) + " " + query + "\n")


read_query()
relevant()
