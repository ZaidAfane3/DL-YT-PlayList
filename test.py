from datetime import datetime


oldformat = '3/1/2014'
datetimeobject = datetime.strptime(oldformat,'%d/%m/%Y').strftime('%d-%m-%Y')
print (datetimeobject)
