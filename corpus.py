from bs4 import BeautifulSoup
import re
import traceback
import os
import glob

file_list = []
dir = 'Corpus'


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


def fetch_data():
    try:
        counter = 1
        for filename in glob.glob(os.path.join('*.html')):
            with open(filename) as f:
                article = filename.strip('cacm/').strip('.html')
                data = f.read()
                counter += 1
                soup = BeautifulSoup(data, 'html.parser')
                soup.prettify().encode('utf-8')
                text = soup.find('text').get_text().encode('utf-8')
                content = text
                processed_data = transformation(content)
                processed_data = processed_data.lower()
                write_file(processed_data, article)
                f.close()
    except:
        print("Try block error")
        print(traceback.format_exc())


def write_file(data, file_name):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
        index_terms = open(dir + '/' + file_name + '.txt', 'w')
        index_terms.write(data)
        index_terms.close()
    except:
        print("Try block error")
        print(traceback.format_exc())
