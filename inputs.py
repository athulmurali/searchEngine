import os


listOfQueries = [\
"hurricane isabel damage",
"forecast models",\
"green energy canada",\
"heavy rains",\
"hurricane music lyrics",\
"accumulated snow",\
"snow accumulation",\
"massive blizzards blizzard",\
"new york city subway"]


#Added for BM 25 --------------------
bm25ResultsFile       = "bm25Results.txt"
bm25ScoredResultsFile = "bm25ScoredResults.txt"



# In each ngram folder, inverted index will be created 
# as a text file with the below name




# Parent folder name of parsed documents:


parent_of_parsed  = "2017_11_8_16_31_29"

master_path 	 =  os.path.join(os.getcwd(), parent_of_parsed);

raw_docs_folder_name	= "raw_documents"
parsed_docs_folder_name = "parsed_documents"

parsed_docs_path = os.path.join(master_path,parsed_docs_folder_name)
# print(parsed_docs_path)



inv_file_name 		= "inverted_index.txt"
sorted_tf_file_name = "sorted_tf.txt"
sorted_df_file_name = "sorted_df.txt"

n_grams_to_do = [1,2,3]
n_grams_to_do = [1]

# changable user data
crawl_delay      = 0;

# crawler_limit sets the number of pages to crawl
# note : No of pages to crawl , not number of links to gener
crawler_limit    = 1000;
depth_required   = 6

seed             = "https://en.wikipedia.org/wiki/Tropical_cyclone"


# Prefix to add specifies the prefix that 
# must be appended to wiki links generated
# All the links generated  starts with /wiki
# To have it as a crawlable link,
# we add https://en.wikipedia.org to /wiki/Tropical_cyclone

prefix_to_add    = "https://en.wikipedia.org"


# prefix must be given as tuples
# examples can be found at the bottom of this script

prefix    			= "/wiki";

prefix_to_remove    = prefix_to_add+ prefix+"/";


# str_to_ignore - list of strings : If the crawler finds 
# a link with one of the following characters in the link
# it skips
str_to_ignore		= [":","*","$","&",".jpg"];




# t = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'));



visited_text_file 			= "visited_links.txt"
url_to_doc_file   			= "url_to_doc_name.json"


in_links_file      			= "in_links.json"
out_links_file     			= "out_links.json"

in_links_doc_id_file      	= "in_links_doc_id.json"
out_links_doc_id_file     	= "out_links_doc_id.json"


# The below parameter sets the name of the new folder that will created inside
# time_dated folder for each crawling
raw_documents_folder        ="raw_documents"


entropy_log_base     = 2
tele_damp_factor     = 0.85
# ======================================================================

# examples

# str = ["a","b","c"];
# a  = "bbbb";

# if any(x in str for x in a):
# 	print("True......")



# tuples:
# abc = "a","b","c"

# word = "avdfg";

# if word.startswith(abc):
# 	print("true");


#Added for CACM retrieval by Athul
#Parser.py uses the following
CACM_PREFIX = "CACM-"