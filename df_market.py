import re
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
ave = int(ave)
print(ave)


