import json
import requests
from bs4 import BeautifulSoup

#step 1 lets create class to get solutions from cchef

class cchef():
	"""docstring for cchef"""
	def __init__(self, username,password):
		self.username = username
		self.password = password
		self.session  = requests.Session()
		self.submissions = {}
	
	def getSubmissions(self):
		url = 'https://www.codechef.com/users/'+self.username
		response = self.session.get(url)
		parsed_response = BeautifulSoup(response.text,'lxml')
		submission_section = parsed_response.find('section',{'class':'rating-data-section problems-solved'})
		for article  in submission_section.findAll('article'):
			plist = article.findAll('p')
			for p in plist:
				problem = {}
				uid = p.find('a').text
				problem['submissions_link'] = p.find('a')['href']
				problem['submissions'] = []		
				response = self.session.get('https://www.codechef.com'+problem['submissions_link']+'?status=15')
				parsed_response = BeautifulSoup(response.text,'lxml')
				submissions = parsed_response.find('tbody').findAll('tr')
				for s in submissions:
					submission = {}
					tds = s.findAll('td')
					submission['id'] = tds[0].text
					submission['lang'] = tds[-2].text
					submission['link'] = tds[-1].find('a')['href']
					problem['submissions'].append(submission)
				self.submissions[uid]=problem
		print(json.dumps(self.submissions,indent=4))

def test_cchef():
	user = cchef('moghya','helpit70.')
	user.getSubmissions()

test_cchef()