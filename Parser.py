import os
import re
from bs4 import BeautifulSoup
import time;

import glob

from file_functions import *;
print (os.getcwd());

source_path 		= os.path.join(master_path, raw_docs_folder_name);
destination_path 	= os.path.join(master_path, parsed_docs_folder_name);
case_folding = True;
ext_to_remove = ".html"
parsed_documents_path = destination_path;

def parse_html_file(file_name):
	
	temp_file = open(file_name,'r',encoding='utf8')
	soup = BeautifulSoup(temp_file, "html.parser");
	temp_str =  soup.title.get_text();

	if soup.h1:
		temp_str = temp_str + " " + soup.h1.get_text();

	if soup.h2:
		temp_str = temp_str + " " + soup.h2.get_text();

	if soup.h3:
		temp_str = temp_str + " " + soup.h3.get_text();

	if soup.h4:
		temp_str = temp_str + " " + soup.h4.get_text();

	if soup.h5:
		temp_str = temp_str + " " + soup.h5.get_text();

	if soup.h6:
		temp_str = temp_str + " " + soup.h6.get_text();

	if soup.h7:
		temp_str = temp_str + " " + soup.h7.get_text();

	if soup.h8:
		temp_str = temp_str + " " + soup.h8.get_text();


	all_p_tags = soup.findAll('p')
	pattern = r'\[.*?\]'

	for i in all_p_tags:
		temp_p_text = i.get_text().strip();
		temp_p_text.replace("\n","")
		temp_p_text = re.sub(pattern, '',temp_p_text)
		
		temp_p_text= temp_p_text.replace("{\displaystyle", '')
		temp_p_text= temp_p_text.translate({ord('{'):None, ord('}'):None})
		temp_p_text= temp_p_text.replace("}", '')
		temp_p_text= temp_p_text.replace("(", '')
		temp_p_text= temp_p_text.replace(")", '')
		temp_p_text= temp_p_text.replace("/", '')
		temp_p_text= temp_p_text.replace("[edit]", '')
		
		# replace multiple white spaces
		temp_p_text = ' '.join(temp_p_text.split())

		temp_str = temp_str + " " + temp_p_text


	# case folding
	if case_folding:

		temp_str = temp_str.casefold()

	pattern = r"(?<!\d)\s*[-\\/,'|.](?!\s*\d)"
	wierd_symbols_pattern = r"[!@#$*%+_;[]]";


	replace_with = ""
	
	temp_str =  re.sub(pattern,replace_with,temp_str)

	# replace_wierd_symbols
	temp_str = temp_str.replace("@" , "")
	temp_str = temp_str.replace("$" , "")
	temp_str = temp_str.replace("^" , "")
	temp_str = temp_str.replace("^" , "")
	temp_str = temp_str.replace("&" , "")
	temp_str = temp_str.replace(";" , "")
	temp_str = temp_str.replace("_",  "")
	temp_str = temp_str.replace('"', '')
	temp_str = temp_str.replace('"', '')
	temp_str = temp_str.replace("'", "")
	temp_str = temp_str.replace("[edit]", "")

	temp_str =  re.sub(wierd_symbols_pattern,replace_with,temp_str);

	# remove multiple white spaces with single space
	temp_str =  re.sub(' +',' ',temp_str)

	# remove dot betweeen words or non numerical pairs 
	temp_str =  re.sub(r'(?<!\d)\s*[\.=:_,]\s*(?!\d)', '', temp_str);
	
	return temp_str;


# This function will parse all the files present in the given parse_directory
# And put the new files in the destination directory

def parse_directory_files(html_files_directory_path, destination_path):
	all_html_files_path = os.path.join(html_files_directory_path ,"*.html")

	all_files_in_dir  = glob.glob(all_html_files_path);

	parsed_folder = create_folder(master_path,parsed_docs_folder_name);

	for file_name in  all_files_in_dir:
		print("Parsing:.html to processed .txt.. ", file_name.replace(html_files_directory_path,""))

		parsed_str = parse_html_file(file_name);

		file_name        = file_name.replace(raw_docs_folder_name,parsed_docs_folder_name)
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

# parse_directory_files(source_path,destination_path);
# print("Parsing completed...........");

getDocumentLengthDict();