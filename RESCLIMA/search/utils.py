import re

def parseUserTextInput(text,categories):
	pattern = re.compile(r'\w+')
	tokens = re.findall(pattern, text)
	ts_query_str = ""
	num_tokens = len(tokens)
	for index, token in enumerate(tokens):
		if(index != num_tokens - 1):
			token += " & "
		ts_query_str += token

	num_categories = len(categories)
	if num_categories==0:
		return ts_query_str

	if(num_tokens>0):
		ts_query_str += " & ("

	for index, category in enumerate(categories):
		category = category.replace(" ","|")
		if(index != num_categories - 1):
			category += " | "
		ts_query_str += category

	if(num_tokens>0):
		ts_query_str += ")"

	return ts_query_str
