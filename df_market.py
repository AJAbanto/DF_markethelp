import re
import gspread
import datetime

from oauth2client.service_account import ServiceAccountCredentials
from robobrowser import RoboBrowser


print('starting up..')

#open browser
browser = RoboBrowser()
browser.open('http://www.hollowprestige.com/explore/marketplace/')

#get search form to submit
srch_frm = browser.get_form(action='/explore/marketplace/')
srch_frm['TradeZone'].value = 'Secronom Bunker'
srch_frm['Category'].value ='Ammo - Rifle'
srch_frm['Search'].value = '12.7mm'

browser.submit_form(srch_frm)


#get output html
html = str(browser.parsed())

html_f = open('html_out.html','w')
html_f.write(html)
html_f.close()


#Get list of data (contaminated)
result = re.findall(r'e">(.*?)</td>',html)
#print(result)


#Filter results
clean_result =[i for i in result if (i != ("Secronom")) if (i!= "12.7mm Rifle Bullets")]
#print(clean_result)


#get lower bound average
#Note relatively unsure if all boxes in lowerbound are fullboxes)
ave = 0

for i in range(5):
	ave +=int(clean_result[i].replace(',',''))
ave *= 1/5
ave = int(ave) #This is average price of the 5 cheapest items on MP


#Logging data into google sheets
print('Appending Info to Google sheets\n')

#accessing APIs
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('df_mp2_logger.json',scope)

#authorizing
client = gspread.authorize(creds) 

#accessing sheets
sheet = client.open('Deadfrontier_Market_analysis').worksheet('12.7mm Ammo')

#preparing data (Time stamp)
time_stamp = datetime.datetime.now() #timestamp
date = time_stamp.strftime('%m/%d/%Y')	#formatting timestamp
time = time_stamp.strftime('%I:%M %p')
Lbound_price = ave	#lowerbound price average

new_row =[date, time ,Lbound_price]
#print(new_row)
sheet.insert_row(new_row)









