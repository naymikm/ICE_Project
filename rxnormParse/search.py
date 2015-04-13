import requests

f = open('stest.txt','r')
flines = f.read().splitlines()
f.close()
out = open('userOut.txt','w')


def searchName(userName,DATE):
	suggest = requests.get('http://rxnav.nlm.nih.gov/REST/spellingsuggestions.json?name='+userName)
	if (suggest.json()['suggestionGroup']['suggestionList'] is None):
		Error = '\nThe term "'+userName+'" has no search result. Please try another term\nor continue without it.\n'
		print Error
		return
	else:
		suggString = suggest.json()['suggestionGroup']['suggestionList']['suggestion'][0]
#		print suggString+'\n'
		search = requests.get('http://rxnav.nlm.nih.gov/REST/approximateTerm.json?term='+suggString)
		rxcuiString = search.json()['approximateGroup']['candidate'][0]['rxcui']
		propertyjson = requests.get('http://rxnav.nlm.nih.gov/REST/rxcui/'+rxcuiString+'/properties.json')
		if propertyjson is None:
			Error2 = '\nThe term "'+userName+'" does not have a valid RxCUI. Please try another term\nor continue without it.\n'
			print 	Error2
		else:	
			out.write(rxcuiString+'\t'+'RXCUI'+'\t'+DATE+'\n')


for line in flines:
	searchName(line.split('\t')[0],line.split('\t')[1])

out.close()