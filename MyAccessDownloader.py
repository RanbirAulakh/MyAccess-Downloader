import requests
import os
import re
import sys
from bs4 import BeautifulSoup
from sys import platform

# it will create new folders in same directory as this script
def createFolder(term, name):
	cwd = os.getcwd() + "/" + term + "-Notes"
	if not os.path.exists(cwd): 
		print("Created a new folder: " + term + "-Notes")
		os.makedirs(cwd)

	cwd = os.getcwd() + "/" + term + "-Notes/" + name
	if not os.path.exists(cwd):
		print("Created a new folder: " + name)
		os.makedirs(cwd)

userId = sys.argv[1]
term = sys.argv[2]

s = requests.session()
r = s.post('https://myaccess.rit.edu/myAccess5/process_login.php', data={"un":userId,"pw":"", "signin":""})
c = (r.content)

soup = BeautifulSoup(c, "html.parser")

# term = ""

# for i in soup.findAll("span"):
# 	if 'term' in i.attrs:
# 		term = i.attrs['term']


ajax_url = r'https://myaccess.rit.edu/myAccess5/home_ajax_classes.php?term=' + term

r = s.get(ajax_url)
c = r.content
soup = BeautifulSoup(c, "html.parser")

for i in soup.findAll("div", attrs={"class":"well"}):
	currentTerm = i.attrs['term']
	classNum = i.attrs['class_num']
	className = i.attrs['event_title'].replace(" ", "-")
	url = r'https://myaccess.rit.edu/myAccess5/CourseNotes.php?term=' + str(currentTerm) + '&classnum=' + str(classNum)
	c = s.get(url).content
	soup = BeautifulSoup(c, "html.parser")
	if("Not Permitted" not in soup):
		# check if directory exists
		createFolder(currentTerm, className)

		# Checking 
		print("Getting notes from " + className)

		# go into directory and check if there is any notes
		existLst = os.listdir(os.getcwd() + "/" + currentTerm + "-Notes/" + className)
		for i in range(len(existLst)):
			existLst[i] = existLst[i].split("_")[2].split(".")[0]

		# now download files from myaccess and do not download the files that is already exist
		getTables = soup.find("table", attrs={"class":"table table-condensed table-bordered"})
		for i in getTables.findAll("tr"):
			spanExist = i.find("span", attrs={"style":"white-space:nowrap;"})
			if(spanExist):
				for j in i.findAll("td"):
					if(j.text == "Notetaker"):
						if(spanExist.text not in existLst):
							for getLinks in i.findAll("a", href=True):
								if(getLinks.text == "Download"):
									url = r'https://myaccess.rit.edu/myAccess5/' + getLinks['href']
									r = s.get(url, stream = True)
									d = r.headers['content-disposition']
									fname = re.findall("filename=(.+)", d)
									dst = os.getcwd() + "/" + currentTerm + "-Notes/" + className + "/" + fname[0]
									print("Downloading: (" + spanExist.text + ") -- " + fname[0])
									with open(dst,"wb") as pdf:
										for chunk in r.iter_content(chunk_size=1024):
											if chunk:
												pdf.write(chunk)









