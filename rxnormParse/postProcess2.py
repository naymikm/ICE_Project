import json, time, os
from datetime import date
path = os.getcwd()
out = open('FINAL_RECONCILE.txt', 'w')
fuzzy = open('FINAL_FUZZY_DATES.txt','w')
fuzzy.write("Fuzzy dates list:\n")
with open(path+'/FINAL_OUTPUT/rec_00001.json') as rec1:
	data = json.load(rec1)

med_len = len(data["reconciled"])
i=0
while i < med_len:
	fuz1=False
	fuz2=False
	normd1=[]
	normd2=[]
	d1 = data["reconciled"][i]["med1"]["instructions"].split('-')
	if len(d1) == 3:
		normd1.append(int(d1[2]))
		normd1.append(int(d1[0]))
		normd1.append(int(d1[1]))
	elif len(d1) == 2:
		normd1.append(int(d1[1]))
		normd1.append(int(d1[0]))
		normd1.append(15)
		fuz1=True
	else:
		fuz1=True
		normd1.append(int(d1[0]))
		normd1.append(6)
		normd1.append(15)
	d2 = data["reconciled"][i]["med2"]["instructions"].split('-')
	if len(d2) == 3:
		normd2.append(int(d2[2]))
		normd2.append(int(d2[0]))
		normd2.append(int(d2[1]))
	elif len(d2) == 2:
		normd2.append(int(d2[1]))
		normd2.append(int(d2[0]))
		normd2.append(15)
		fuz2=True
	else:
		fuz2=True
		normd2.append(int(d2[0]))
		normd2.append(6)
		normd2.append(15)
	date1 = date(normd1[0], normd1[1], normd1[2])
	date2 = date(normd2[0], normd2[1], normd2[2])
	if date1 == date2:
		out.write(data["reconciled"][i]["med2"]["original_string"]+'\n')
	elif date1.month == date2.month and date1.year == date2.year:
		out.write(data["reconciled"][i]["med2"]["original_string"]+'\n')
	else:
		out.write(data["reconciled"][i]["med2"]["original_string"]+'\n')
		out.write(data["reconciled"][i]["med1"]["original_string"]+'\n')
		
	if fuz1 == True or fuz2 == True:
		fuzzy.write(data["reconciled"][i]["med2"]["original_string"]+' : ')
		fuzzy.write(data["reconciled"][i]["med1"]["original_string"]+'\n')
	else:
		pass
	i+=1

l1 = len(data["new_list_1"])
i1 = 0
while i1 < l1:
	out.write(data["new_list_1"][i1]["original_string"]+'\n')
	i1+=1

l2 = len(data["new_list_2"])
i2 = 0
while i2 < l2:
	out.write(data["new_list_2"][i2]["original_string"]+'\n')
	i2+=1
out.close()