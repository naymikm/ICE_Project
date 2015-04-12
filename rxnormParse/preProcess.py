import requests

vmr1 = open('testvMRout.txt', 'r')		# loads input files
vmr2 = open('testvMRout2.txt','r')
vmrLines1 = vmr1.read().splitlines()	# reads each line and adds it as an element to a list
vmrLines2 = vmr2.read().splitlines()
vmr1.close()
vmr2.close()							# closes text files; no longer neded in memory.
#print vmrLines1
out = open('TEST.txt','w')				# initiates output file

def getName(idCode,idType,DATE):
	#print idCode+' '+idType
	rxjson = requests.get('http://rxnav.nlm.nih.gov/REST/rxcui.json?idtype='+idType+'&id='+idCode)			# queries rxnorm using alternative code
	rxcuiString = rxjson.json()['idGroup']['rxnormId'][0]													# parses the json from query for the RXCUI code
	propertyjson = requests.get('http://rxnav.nlm.nih.gov/REST/rxcui/'+rxcuiString+'/properties.json')		# queries rxnorm using the rxcui for the RxNorm name
	rxNameString = propertyjson.json()['properties']['name']												# parses the json for the RxNorm name
	out.write(rxNameString+' 0 MG injectable;'+DATE+'\n')			# write to output file in MedRec specific format
	


for line in vmrLines1:						
	#print line
	idCode = line.split('\t')[0]
		#print '\n'+idCode
	idType = line.split('\t')[1]						# gets the code, type of code, and date from the input filesList
		#print '\n'+idType 								# and feeds them to the function above for querying RxNorm
	DATE = line.split('\t')[2]	
	getName(idCode,idType,DATE)

out.write('******\n')									# split the lists in the output file by asteriks 

for line in vmrLines2:
	#print line
	idCode = line.split('\t')[0]						# same thing but for file 2
		#print '\n'+idCode
	idType = line.split('\t')[1]
		#print '\n'+idType
	DATE = line.split('\t')[2]	
	getName(idCode,idType,DATE)

out.write('******')
out.close()												# closes output file saving it