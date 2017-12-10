import os
import re
from bs4 import BeautifulSoup
import time;

import glob

from inputs import *
from file_functions import *;
from CommonUtils import *;


print (os.getcwd());

source_path 		= os.path.join(master_path, raw_docs_folder_name);
destination_path 	= os.path.join(master_path, parsed_docs_folder_name);
case_folding = True;
ext_to_remove = ".html"
parsed_documents_path = destination_path;



#Added by :Athul
# This function is applicable for cacm form only
#fetches the data from .html files in cacm
#returns a string from a html file
def fetch_cacm_data(file_name):
	temp_file = open(file_name,'r',encoding='utf8')
	soup = BeautifulSoup(temp_file, "html.parser");

	temp_str = ""
	soup.html.findAll('pre')

	soup.prettify().encode('utf-8')
	text =str(soup.find('pre').get_text())
	# print(text)
	# print( "transformed ",transformation(text))
	return text;


# This function will parse all the files present in the given parse_directory
# And put the new files in the destination directory

def parse_directory_files(html_files_directory_path, destination_path):
	all_html_files_path = os.path.join(html_files_directory_path ,"*.html")

	all_files_in_dir  = glob.glob(all_html_files_path);

	parsed_folder = create_folder(master_path,parsed_docs_folder_name);

	for file_name in  all_files_in_dir:
		print("Parsing:.html to processed .txt.. ", file_name.replace(html_files_directory_path,""))

		# parsed_str = parse_html_file(file_name);
		parsed_str = fetch_cacm_data(file_name)
		parsed_str = parsed_str.casefold()

		file_name        = file_name.replace(raw_docs_folder_name,parsed_docs_folder_name)
		file_name        = file_name.replace(CACM_PREFIX,"")
		parsed_file_name = file_name.replace(".html", ".txt");
		string_to_text_file(parsed_file_name,parsed_str);
	return 0

# testing functions above

# **********************************************************
#  getDocumentLengthDict(): 
# given 
# source_path		:
# destination_path	:


# returns the document length for each doucment in the given folder 
# example
# dict {1 : 20, 2: 30}
# **********************************************************
def getDocumentLengthDict():
	docLengthDict = {}
	all_txt_files_path = os.path.join(parsed_documents_path ,"*.txt")
	all_files_in_dir  = glob.glob(all_txt_files_path);
	txtExt = ".txt"

	for file_name in  all_files_in_dir:
		docTxt =  text_file_to_string(file_name);
		docLength = len (docTxt.split());
		file_name = str(os.path.basename(file_name));
		doc_id  = file_name.replace(txtExt,""); #without extension
		# print(doc_id, "   ", docLength);
		docLengthDict[doc_id] = docLength;
	# print("docdictSize : ",  len(docLengthDict))
	return docLengthDict;


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Uncomment the following to reparse the text from html folder
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# doc_id_file_name_dict = createDocIDFileNameDict(source_path)
# dict_to_json_file(doc_id_file_name_dict, url_to_doc_file)
# parse_directory_files(source_path,destination_path);
# print("Parsing completed...........");
# print("Doc length : ", getDocumentLengthDict());
