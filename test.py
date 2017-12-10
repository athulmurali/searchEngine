st = "str"

ar = st.split(" ")
print(ar)

import nltk
sno = nltk.stem.SnowballStemmer('english')
print(sno.stem('grows'))



	pattern = r'\[.*?\]'


	temp_p_text = temp_p_text.strip();
	temp_p_text.replace("\n","")
	temp_p_text = re.sub(pattern, '',temp_p_text)
	
	# temp_p_text= temp_p_text.translate({ord('{'):None, ord('}'):None})
	temp_p_text= temp_p_text.replace("}", '')
	temp_p_text= temp_p_text.replace("(", '')
	temp_p_text= temp_p_text.replace(")", '')
	temp_p_text= temp_p_text.replace("/", '')
	temp_p_text= temp_p_text.replace("[edit]", '')
	
	# replace multiple white spaces
	temp_p_text = ' '.join(temp_p_text.split())

	temp_str = temp_str + " " + temp_p_text


	# case folding
	# if case_folding:

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
