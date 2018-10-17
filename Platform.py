import sys
import requests
import json
import datetime
import mysql.connector 
import smtplib
import config
from bs4 import BeautifulSoup 


sys.path.append("./BeautifulSoup")


#API KEY For Scrapping
apikey = "2db16505"


#Assigning ID to each month 
month_val = {'Jan.' : 1, 'Feb.' : 2, 'Mar.' : 3, 'Apr.' : 4,'May.' : 5, 'Jun.' : 6, 'Jul.' : 7,
 'Aug.' : 8, 'Sep.' : 9, 'Oct.' : 10, 'Nov.' : 11, 'Dec.' : 12 }

# Function to send email

def send_email(receiver,message,subject):
	try :
		server = smtplib.SMTP('smtp.gmail.com',587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(config.email,config.password ) 
		message = "Subject : {}  \n\n  {}".format(subject,message)
		server.sendmail(config.email,receiver,message)
		server.quit()
		print("Email Sent to " + str(receiver) )
	except:
		print("Sorry The email can't be send")


# connect to MYSQLdb  

def connect_to_db():
	mydb = mysql.connector.connect(
		host = "localhost",
		user = "root",
		password = "root",
		database = "db1"
	)
	return mydb


def scraper(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.content,"html.parser")
	return soup



mydb = connect_to_db()
mycursor = mydb.cursor()


email = raw_input(" Enter your email-id  ")
TVseries = raw_input("Enter TV series you like seperated by ' , ' \n")


query = "INSERT INTO user (email,series) VALUES (%s,%s)"
values = (email,TVseries)
mycursor.execute(query,values)
mydb.commit()

TVseries = TVseries.split(',')

series_status = {}
series_id_rel = {}
Series_ID = []

for item in TVseries:
	item = item.lstrip()										##Customize input 
	item = item.rstrip()
	item = item.lower()
	words = item.split(" ")
	item = ""			
	for l in words:  
		item  = item + l.capitalize() + " "
	item = item.rstrip()
	key = item							
	url = "http://www.omdbapi.com/"
	item =  item.replace(" ","+")
	url = url + '?s=' + str(item) + "&type=series" + '&apikey=' + str(apikey)
	try:
		soup = scraper(url)
		newDict = json.loads(str(soup))
		ID = newDict['Search'][0]['imdbID']
		Series_ID.append(ID)
		series_id_rel[str(ID)] = key
	except:
		print(item + " is not a valid series name")

for item in Series_ID:
	url = "https://www.imdb.com/title/"
	url = url + str(item) + "/"
	soup = scraper(url)
	z = soup.find("div",{"class" : "seasons-and-year-nav"})
	ses_info = z.contents		
	date= ses_info[9].contents							
 	today = datetime.datetime.now()								
  	count = 0
  	season_year_list = [] 
	for year in date:
	 	if(count%2 == 1 and count < len(date)-2):
  		 	if(int(year.contents[0]) >= int(today.year)):
  		 		season_year_list.append(year.get("href"))
  		count = count + 1


  	if len(season_year_list) == 0 :
		text = "The show has finished streaming all its episodes."
		series_status[series_id_rel[str(item)]] = text
  	else:
  		for i in reversed(season_year_list): 						
			link = "https://www.imdb.com" + str(i)
			response = requests.get(link)
			soup = BeautifulSoup(response.content,"html.parser")
			z = soup.find_all("div",{"class" : "airdate"})
			flag = False	
			for elements in z:
				episode_date = elements.contents[0].encode('utf-8')
				episode_date = str(episode_date).lstrip()
				showDate = episode_date.split(' ')
				airMonth = month_val.get(str(showDate[1]))
				airDate = showDate[0]
				curr_month = month_val.get(today.strftime("%b") + '.') 
				curr_date = today.strftime("%d")
				if( curr_month > airMonth ):
					continue
				elif (curr_month == airMonth ):
					if(int(curr_date) <= int(airDate) ):
						text = "The next episode airs on " + str(airDate) + "-" + str(airMonth) + "-"+ str(ses_year)
						series_status[series_id_rel[str(item)]] = text
						flag = True
						break
					else :
						continue				
				else:
					text = "The next episode airs on " + str(airDate) + "-" + str(airMonth) + "-"+ str(ses_year)
					series_status[series_id_rel[str(item)]] = text
					flag = True				
					break
			if(flag == False and len(season_year_list) == 2 ):
				text = "The next season begins in " + str(int(today.year + 1))
				series_status[series_id_rel[str(item)]] = text
			else:
				text = "The show has finished streaming all its episodes."
				series_status[series_id_rel[str(item)]] = text
		#construct message to send to User
message =""
subject ="Your Tv series Details"

for element in series_status:
	message = message + str(element).upper() + '-' +series_status[str(element)]+ "\n\n"

send_email(email,message,subject)











