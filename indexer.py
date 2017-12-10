from collections import Counter,defaultdict
import os,glob
from file_functions import *
from inputs import *

# File paths
parsed_documents_path = os.path.join(master_path, parsed_docs_folder_name);


# ================================================
# token_count_dict is a dictionary
# where,
# key   = String, 
#          representing the document_id
# value = Integer,
 #          representing the number of tokens
 #           in the document with its key as name

# ==================================================
token_count_dict ={}
file_extension = ".txt"

def str_to_n_grams(str,ngrams_to_do):
	
	output_list = []
	current_n_gram_list = [];
	word_n_gram = [];
	for i in ngrams_to_do:
		print("Processing: word-",i,"-gram" )
		current_n_gram_list = return_word_n_grams(str,int(i));
		total_tokens =  len(current_n_gram_list);
		print("total_tokens : ",total_tokens);

		output_list.append(current_n_gram_list);
	return word_n_gram;

# =====================================================================
# return_word_n_grams : String Integer => StringList
# str - String,
#      represents the string for which word_n_gram has to be returned

# n   - Integer,
#      represents the number of grams or words 
#      seperated by the same delimiter


# returns : StringList,
#           each string representing a word_n_gram for the given n
#           if n is 1, then it will be a list of unigrams,
#           if n is 2, then it will be a list of bigrams

# **************************************************************
def return_word_n_grams(str,n):

	word_n_gram_list = []; 
	str_in_list = str.split(" ");

	while str_in_list:

		token = ""
		
		for i in range(0,n):
			if str_in_list:
				token = token + " " +str_in_list.pop(0);
		# print("token : ",token );

		token_to_append = token.strip();
		if token_to_append is not "":

			word_n_gram_list.append(token_to_append);

	return word_n_gram_list;

# ==========================================================
# calc_term_frequency : StringList => Dictionary
# term_list - StringList, 
#            Could be a word-1-gram, 2-gram or "" list

# returns - A dictionary with each unique term as key and its count as value


def calc_term_frequency(dict_inv_ind):
	print("calculating term frequency")
	dict_term_frequency = {};

	for key in dict_inv_ind:
		new_key = key.strip();
		values  = dict_inv_ind[key];
		# The number of term occurences are always 
		# in the second index of the tuple
		count_list =list(zip(*values))[1] #reprents the list of word frequency in each term

		term_total_count = sum(count_list)

		dict_term_frequency[new_key] = term_total_count

	print("end of loop" )
	return dict_term_frequency;

# =======================================================

def build_inverted_index(source_directory, words_n_gram):

	all_html_files_path = os.path.join(source_directory,"*.txt");
	all_files_in_dir    = glob.glob(all_html_files_path);
	print(all_html_files_path);

	term_frequenies = defaultdict(list);

	for file_name in all_files_in_dir:
		str_from_file  		= text_file_to_string(file_name);
		n_grammed_list 		= return_word_n_grams(str_from_file,words_n_gram);
		counted_terms_dict  = dict(Counter(n_grammed_list));

		file_name = os.path.basename(file_name);
		print("Entering ....",file_name)

		doc_id =  file_name.replace(file_extension,"")
		print(doc_id);
		# print(doc_id)
		doc_id = int(doc_id)

		for term in counted_terms_dict:
			term_count =  counted_terms_dict[term];
			tf_tuple = (doc_id,term_count);

			if term_frequenies[term]:
				term_frequenies[term] = term_frequenies[term] + ((tf_tuple),)
			else:
				term_frequenies[term] = ((tf_tuple),)	

			# print(term, " : ",(term_frequenies[term]));
	return term_frequenies;

def sort_tf_freq(dict_term_frequency):
	print("Sorting tf... ");
	tf_tuples =  dict_term_frequency.items();

	sorted_tf = sorted(dict_term_frequency.items(), \
		key=lambda k_v:  int(k_v[1]), reverse=True)
	print("returned - sorted tf... ");

	return sorted_tf;

def alpha_sort_dict_to_tuples(dict_term_frequency):
	print("Sorting... df lexicographically ")

	alpha_sorted = sorted(dict_term_frequency.items(), key=lambda k_v:  str(k_v[0]))
	return alpha_sorted;

def return_df_dict(inv_ind_dict):
	print("Generating df table")
	df_dict = {}
	for term in inv_ind_dict:
		docs_with_term  = []
		
		# values will be a tuple of  tuples
		values          = inv_ind_dict[term]
		for tup in values:
			# tup[0] will be containing the document id
			docs_with_term.append(tup[0])

		docs_count      =  len(docs_with_term);
		df_dict[term]   =  (docs_with_term,docs_count)
	return df_dict;
 

# ===============Tested the above functions===============================
# The below array descirbes for 
# str_test = "abc def ghi jkl mno abc def"
# n_grams_to_do = [1,2,3]
# str_to_n_grams(str_test, [1,2]);
# counted_terms = Counter(return_word_n_grams(str_test,1));

# print(dict(counted_terms));


# tasks-by-n-gram
# for each n-gram,
# Create  a folder  like 1_gram

# generate an inverted index  - inside the folder 


def tasks_by_n_gram(master_path,n_gram_list):
	# For creating folder we need a prefix
	# that iterates for each n gram

	for i in n_gram_list:
		print("Processing ...  " + str(i)+ "_gram")
		n_gram_prefix = str(i) + "_gram";
		
		folder_name 		=  n_gram_prefix
		folder_path 		= create_folder(master_path,folder_name);

		inv_ind 			= build_inverted_index(parsed_documents_path,i);

		inv_file_path   	=  os.path.join(folder_path ,inv_file_name)
			
		dict_to_text_file(inv_ind,inv_file_path);

		dict_term_frequency = calc_term_frequency(inv_ind);
		print("Successfully returned tf unsorted")
		sorted_tf 			= sort_tf_freq(dict_term_frequency);
		print("Successfully returned sorted_tf")
		sorted_tf_length	= len(sorted_tf);
		print("length of sorted tf: ", len(sorted_tf))
		sorted_tf_file_path = os.path.join( folder_path,sorted_tf_file_name)  ;
		tf_tuples_to_text_file(sorted_tf,sorted_tf_file_path);

		
		df_dict                   = return_df_dict(inv_ind);
		alpha_sorted_df_dict      = alpha_sort_dict_to_tuples(df_dict);
		sorted_df_file_path       = os.path.join( folder_path,sorted_df_file_name)  ;
		df_tuples_to_text_file(alpha_sorted_df_dict,sorted_df_file_path); 

	return;


#Uncomment the following to build index 
# tasks_by_n_gram(master_path,n_grams_to_do);