import requests

f = open('userInput.txt','r')
flines = f.read().splitlines()
f.close()
out = open('userOut.txt','w')
out2 = open('noTerms.txt','w')


#add a loop for approximate terms

def getInput(slist):
	inpt = int(raw_input("Enter the number of the correct term:	"))
	if inpt not in range(0,len(slist)):
		print 'Please enter a number between 0 and '+str(len(slist)-1)
		return getInput(slist)
	else:
		print '\nYou chose '+str(slist[inpt])
		choose = raw_input('Is this correct? [Y/N]') 
		if choose.upper() not in ['Y','YES']:
			return getInput(slist)
		else:
			return inpt

def suggestName(userName,DATE):
	suggest = requests.get('http://rxnav.nlm.nih.gov/REST/spellingsuggestions.json?name='+userName)
	if (suggest.json()['suggestionGroup']['suggestionList'] is None):
		Error = '\nThe term "'+userName+'" had no search result. Will attempt to use raw input.\n'
		print Error
		out2.write(userName+'\t'+DATE+'\n')
		return userName
	else:
		print 'You listed\t'+userName+'\n'
		suggestList = suggest.json()['suggestionGroup']['suggestionList']['suggestion']
		i = 0
		while i < len(suggestList):
			print str(i)+'\t.....\t'+str(suggestList[i])+'\n'
			i+=1
		return suggestList[getInput(suggestList)]
		print '----------------------------------'


def searchName(sName,DATE):
		suggString = suggestName(sName,DATE)
		search = requests.get('http://rxnav.nlm.nih.gov/REST/approximateTerm.json?term='+suggString)
		if 'candidate' not in search.json()['approximateGroup']:
			out2.write(sName+'\t'+DATE)
		else:	
			searchList = search.json()['approximateGroup']['candidate']
			i = 0
			while i < len(searchList):
				rxcuiString = searchList[i]['rxcui']
				propertyjson = requests.get('http://rxnav.nlm.nih.gov/REST/rxcui/'+rxcuiString+'/properties.json')
				if propertyjson.json() is None:
					i+=1
					continue
				else:
					print 'Found RxCUI: '+rxcuiString+' for the item '+'"'+suggString+'" moving to next item...' 
					print '\n-----------------------------------\n'
					out.write(rxcuiString+'\t'+'RXCUI'+'\t'+DATE+'\n')
					break


for line in flines:
	userInputName = line.split('\t')[0]
	userInputDate = line.split('\t')[1]
	searchName(userInputName,userInputDate)


out.close()
out2.close()