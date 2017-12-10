from bs4 import BeautifulSoup
import re
import traceback
import os
import glob

from inputs import *

#Add functions below with your name in the function header
#Contains functions that can be used by all other modules
#For example, writeDictoJson, readFromFile,etc


# the following functino applies to CACM only. This has to be changed 
# Below the file name must be given withour location:
# For example
# if the actual file_name is 
# D:\\MS_Computer_Science\\IR\\Assignments\\Project\\searchEngine\\2017_11_8_16_31_29\\raw_documents\\CACM-3204.html'
# the file_name passed to the function must be CACM-3204.html
# file_path : 'CACM-' THe  prefix that is present in each and every file_name
# that is to be removed before creating a doc_id




#Function created by: Meghna
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

#Function created by: Meghna
def handle_punctuation(term):
    while term[:1] == "-" or term[:1] == "," or term[:1] == ".":
        if re.match(r'^[\-]?[0-9]*\.?[0-9]+$', term):
            return term
        if term[:1] == "-" or term[:1] == "." or term[:1] == ",":
            term = term[1:]
        else:
            return term
    return term

#returns a dict :
# key   : doc_id
# value : file_name of html doc with path
def createDocIDFileNameDict(html_files_directory_path):
	all_html_files_path = os.path.join(html_files_directory_path ,"*.html")
	all_files_in_dir  = glob.glob(all_html_files_path);
	doc_id_file_name_dict = {}
	for file_name in  all_files_in_dir:
		
		doc_id	= os.path.basename(file_name);
		doc_id = str.replace(doc_id,CACM_PREFIX,"")
		doc_id = doc_id.replace(".html","")
		doc_id_file_name_dict[str(doc_id)] =  str(file_name);
		# print(doc_id, str(file_name))
	return doc_id_file_name_dict;






def fileNameTodocID(file_name,file_path,extension):
	file_name.replace(file_path , "" )
	file_name.extension(extension, "")
	return file_name