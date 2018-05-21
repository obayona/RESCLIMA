
def import_data(request):
	list_files = request.FILES.getlist('import_files')
	title = request.POST["title"]
	abstract = request.POST["abstract"]

	print title
	print abstract

	
	for i in list_files:
		print i

	return None