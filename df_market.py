import re
import gspread
import datetime
from datetime import datetime
from datetime import timedelta

import ntplib
import time
from oauth2client.service_account import ServiceAccountCredentials
from robobrowser import RoboBrowser


print('starting up..')
while True:
	#open browser
	browser = RoboBrowser(parser='lxml') #parser set to lxml as recommended to supress warnings
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
	#print('Appending Info to Google sheets\n')

	#accessing APIs
	scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name('api_keys/df_mp2_logger.json',scope)

	#authorizing
	client = gspread.authorize(creds) 

	#accessing sheets
	sheet = client.open('Deadfrontier_Market_analysis').worksheet('12.7mm Ammo')

	#preparing data (Time stamp)
	
	try:
		#connecting to ntp server 
		c = ntplib.NTPClient()
		rep = c.request('ph.pool.ntp.org',version=3) #sending request to server
		rep.offset
		time_stamp = datetime.fromtimestamp(rep.tx_time) # + timedelta(hours=8) add hour offset if timezone is wrong 

		date_now = time_stamp.strftime('%m/%d/%Y')	#formatting timestamp
		time_now = time_stamp.strftime('%I:%M %p')

	except:
		date_now = 'Server time_out'
		time_now = 'Server time_out'
			
	Lbound_price = ave	#lowerbound price average
	new_row =[date_now, time_now ,Lbound_price]
	print('New Data: ',new_row)
	sheet.insert_row(new_row)
	print('Cycle Done')
	
	#sleep for 10mins
	for i in range(10):
		time.sleep(60)







