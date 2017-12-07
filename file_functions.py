try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

# from urllib2 import Request, urlopen

import os.path
import datetime

import urllib
import re
from time import sleep;
import json,sys,os
from datetime import datetime
from inputs import *;

# from bs4 import BeautifulSoup, SoupStrainer


def next_document_name(last_document_name):
	return (last_document_name + 1);

def url_doc_name_update( url_doc_dict,url,document_name):
	if url in url_doc_dict:
		return url_doc_dict.get(url);

	else:
		doc_name = next_document_name(document_name);
		print("docname",doc_name);
		url_doc_dict[url] = doc_name;
		return doc_name;

def dict_to_json_file(dict, file_name):
	
	with open(file_name, "w", encoding="utf-8") as fp:
		json.dump(dict, fp, indent = 4);

def url_doc_name_to_file(url_doc_dict):
	
	with open('result.json', "w", encoding="utf-8") as fp:
		json.dump(url_doc_dict, fp, indent = 4);


def in_links_dict(in_links_file):	
	with open(in_links_file , "w", encoding="utf-8") as fp:
		json.dump(url_doc_dict, fp, indent = 4);


def visited_list_to_file(visited_list):
	thefile = open(visited_text_file, "w", encoding="utf-8");
	for i in visited_list:
		thefile.write("%s\n" %i);

def update_in_links_dict(in_links_dict, parent, children):

	for  child in children:

		if child in in_links_dict:
			
			in_links_dict[child].append(str(parent));

			temp_in_links = in_links_dict[child];
			temp_in_links = ( list (set (temp_in_links)))

			in_links_dict[child] = temp_in_links;
		else:
			
			in_links_dict[child] = [parent];



def update_out_links_dict(out_links_dict, parent, children):
	temp_children = [];

	print("outlinks----------------------------")
	print("parent   :",  str(parent) );
	print("children");
	for c in children: print(str(c));
	
	for child in children:
		if (str(parent) != str(child)):
			temp_children.append(child);


		if parent in out_links_dict:
			temp_out_links 		= out_links_dict[parent];
			temp_out_links 		= temp_out_links.append(temp_children);

		else:			
			temp_out_links = temp_children ;



		if temp_out_links:
			temp_out_links        =  (list (set (temp_out_links)));
		else:
			temp_out_links        =[];

		out_links_dict[parent] = temp_out_links;
		return;

def in_links_remove_unvisited_keys( visited_list, in_links_dict ):
	
 	for k in in_links_dict.keys():
 		
 		if k not in visited_list:
 			del in_links_dict[k];
 	return in_links_dict;
 

def keys_count_links(json_file):
	with open(json_file, "r", encoding="utf-8") as fp:
		temp_dict = json.load(fp);
	print("total_keys in the json file:    ", len(temp_dict));

def load_json_to_dict(file_name):
	with open(file_name, "r", encoding="utf-8") as fp:
		temp_dict = json.load(fp);
		return temp_dict;



def add_inlink_to_dict(in_links_dict, parent, child):

	if child in in_links_dict:
		
		in_links_dict[child].append(parent);

		temp_in_links = in_links_dict[child];
		temp_in_links = ( list (set (temp_in_links)))

		in_links_dict[child] = temp_in_links;
	else:
		
		in_links_dict[child] = [parent];


# Converts the dict with urls to docname dict


def url_dict_to_docID(url_dict):
	new_values = [];
	dict_of_docID = {}

	for key in url_dict:

		new_key = str(key);
		new_key = url_to_docID(key);
		

		temp_values =url_dict[key];
		formatted_temp_values = []

		for val in temp_values: formatted_temp_values.append(str(val));

		new_values = [];
		for val  in formatted_temp_values:

			new_values.append(url_to_docID(val));
			dict_of_docID[new_key] = new_values;
	return dict_of_docID;


def json_file_to_dict(json_file):

	new_dict= {};
	with open(json_file, "r", encoding="utf-8") as fp:
		new_dict = json.load(fp);
		return new_dict

	

def url_to_docID(url):
	return url.replace(prefix_to_remove,"");



# converts keys as values and values as keys
def reverse_map_dict(input_dict):

	new_dict = {};

	for key in input_dict:
		

		old_values = input_dict[key];

		new_value = key	


		for new_key in old_values:
			temp_new_values =[];
			
			if new_key in new_dict:
				temp_new_values     = new_dict[new_key]
				temp_new_values.append(new_value)
				temp_new_dict_values = ( list (set (temp_new_values)))

			else:
				temp_new_values.append(new_value) ;

			new_dict[new_key] = temp_new_values;

	return new_dict;


# Generate a folder_name with the current date_time till seconds
# Create a folder with the current_folder_name

# Add all  downloaded web pages to that folder

def create_folder(folder_location,folder_name):
	final_directory = os.path.join(folder_location,folder_name)
	if not os.path.exists(final_directory):
   		os.makedirs(final_directory)

	return final_directory;

def generate_folder_name():
	current_date_time = datetime.datetime.now();

	current_year  = str(current_date_time.year)
	current_month = str(current_date_time.month)
	current_day   = str(current_date_time.day)
	current_hour  = str(current_date_time.strftime('%H'))
	current_min   = str(current_date_time.strftime('%M'))
	current_sec   = str(current_date_time.strftime('%S'))


	folder_name = str (current_year + "_" + current_month + "_" + current_day + "_"+\
	 current_hour+"_" + current_min +"_" + current_sec);

	return (folder_name);

def download_webpage(url,file_name):
	print("URL in download page: ",url)
	q = Request(str(url))
	q.add_header('User-Agent', 'Mozilla/5.0')
	r = urlopen(q).read()
	soup = BeautifulSoup(r, "html.parser")
	with open(file_name, "w", encoding="utf-8") as f:
		f.write(str(soup))
		f.close()
	return soup;


def return_filename_with_location(folder_location,file_name):
	return os.path.join(folder_location,file_location);

# file_name_with_location = os.path.join(file_location,url_to_docID()),


def text_file_to_string(file_name):
	with open(file_name, 'r', encoding="utf-8") as myfile:
		return myfile.read().replace('\n', '')

def string_to_text_file(file_name,str):
	with open(file_name, "w", encoding="utf-8") as text_file:
		text_file.write(str)
	return 0;		

def dict_to_json_file_indented(dict, file_name,indent):
	
	with open(file_name, "w", encoding="utf-8") as fp:
		json.dump(dict, fp, indent = indent);

def inverted_index_to_string(inv_ind):
	str_out = "";

	for key in inv_ind:
		current_row = str_out + str(key) + " : " + str(inv_ind[key]) +"\n";
		str_out = str_out + current_row;
	str_out.strip();
	return str_out;


def dict_to_text_file(inv_dict,file_name):

	# Removing the file to avoid appending to the old file
	
	remove_file_if_exists(file_name);
	
	with open(file_name,"a", encoding='utf8') as fp:
		for key in inv_dict:
			current_row = str(key) + " : " + str(inv_dict[key]) +"\n";
			fp.write(current_row);
	return 0;

def tf_tuples_to_text_file(tf_tuples,file_name):
	
	remove_file_if_exists(file_name);

	with open(file_name, "a", encoding="utf-8") as fp:
		for t in tf_tuples:
			str_out = str(t[0]) + " : " + str(t[1]) + "\n";
			fp.write(str_out);
	return 0;

def df_tuples_to_text_file(tf_tuples,file_name):

	remove_file_if_exists(file_name);
	with open(file_name, "a", encoding="utf-8") as fp:
		for t in tf_tuples:
			str_out = \
			(t[0]) + " : " + \
			str(t[1][0]) +  " "  +\
			str(t[1][1]) +  "\n";
			fp.write(str_out);
	return 0;

def remove_file_if_exists(folder_path_with_name):
	if os.path.exists(folder_path_with_name):
		os.remove(folder_path_with_name);


# Added for BM 25=============================================
def getdocIdList():
	docIdDict = json_file_to_dict(url_to_doc_file);
	# the current json file contains docId as 0.html, 1.html
	# so the html extension must be removed
	docIdList = [];
	for key in docIdDict:
		keyAsStr = str(key)
		keyAsStr = keyAsStr.replace(".html","");
		docIdList.append(keyAsStr)
	return docIdList