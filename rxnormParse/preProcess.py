import requests

vmr1 = open('testvMRout.txt', 'r')		
vmr2 = open('testvMRout2.txt','r')
user = open('userOut.txt','r')
vmrLines1 = vmr1.read().splitlines()	
vmrLines2 = vmr2.read().splitlines()
userLines = user.read().splitlines()
vmr1.close()
vmr2.close()							
noTerm = open('noTerms.txt', 'r')
noTermlines = noTerm.read().splitlines()
noTerm.close()
out = open('officialImmList.txt','w')
out2 = open('userImmList.txt','w')				

# def searchName(userName) in search.py ....



def getName(idCode,idType,DATE):
	#print idCode+' '+idType
	if idType != 'RXCUI':
		rxjson = requests.get('http://rxnav.nlm.nih.gov/REST/rxcui.json?idtype='+idType+'&id='+idCode)				
		rxcuiString = rxjson.json()['idGroup']['rxnormId'][0]														
		propertyjson = requests.get('http://rxnav.nlm.nih.gov/REST/rxcui/'+rxcuiString+'/properties.json')		
		rxNameString = propertyjson.json()['properties']['name']
		if 'MG' in rxNameString.split(' '):
			out.write(rxNameString+' injectable;'+DATE+'\n')
		else:
			out.write(rxNameString+' 0 MG injectable;'+DATE+'\n')
	else:
		propertyjson = requests.get('http://rxnav.nlm.nih.gov/REST/rxcui/'+idCode+'/properties.json')		
		rxNameString = propertyjson.json()['properties']['name']
		if 'MG' in rxNameString.split(' '):
			out.write(rxNameString+' injectable;'+DATE+'\n')
		else:
			out.write(rxNameString+' 0 MG injectable;'+DATE+'\n')

def getName2(idCode,idType,DATE):
	#print idCode+' '+idType
	if idType != 'RXCUI':
		rxjson = requests.get('http://rxnav.nlm.nih.gov/REST/rxcui.json?idtype='+idType+'&id='+idCode)				
		rxcuiString = rxjson.json()['idGroup']['rxnormId'][0]														
		propertyjson = requests.get('http://rxnav.nlm.nih.gov/REST/rxcui/'+rxcuiString+'/properties.json')		
		rxNameString = propertyjson.json()['properties']['name']
		if 'MG' in rxNameString.split(' '):
			out2.write(rxNameString+' injectable;'+DATE+'\n')
		else:
			out2.write(rxNameString+' 0 MG injectable;'+DATE+'\n')
	else:
		propertyjson = requests.get('http://rxnav.nlm.nih.gov/REST/rxcui/'+idCode+'/properties.json')		
		rxNameString = propertyjson.json()['properties']['name']
		if 'MG' in rxNameString.split(' '):
			out2.write(rxNameString+' injectable;'+DATE+'\n')
		else:
			out2.write(rxNameString+' 0 MG injectable;'+DATE+'\n')



for line in vmrLines1:						
	#print line
	idCode = line.split('\t')[0]
		#print '\n'+idCode
	idType = line.split('\t')[1]						
		#print '\n'+idType 								
	DATE = line.split('\t')[2]	
	getName(idCode,idType,DATE)

out.write('******\n')									 

for line in vmrLines2:
	#print line
	idCode = line.split('\t')[0]						
		#print '\n'+idCode
	idType = line.split('\t')[1]
		#print '\n'+idType
	DATE = line.split('\t')[2]	
	getName(idCode,idType,DATE)

out.write('******')

for line in userLines:
	#print line
	idCode = line.split('\t')[0]						
		#print '\n'+idCode
	idType = line.split('\t')[1]
		#print '\n'+idType
	DATE = line.split('\t')[2]	
	getName2(idCode,idType,DATE)

for line in noTermlines:
	out2.write(line.split('\t')[0] + ' 0 MG injectable;' + line.split('\t')[1]+'\n')

out2.write('******')
out2.close()
out.close()												