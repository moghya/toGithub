import json
import requests
from bs4 import  BeautifulSoup
from scrape.scraper import *
from github import Github,GithubException

#let's create a class to test Github API and add functions required for upload files etc.
#we'll use already developed wrapper Github
class upToGithub:
	def __init__(self,username,password):
		self.session  = requests.Session()
		self.username = username
		self.password = password
		self.repoDesc = 'This repository contains submissions made on websites like Hackerrank,Hackerearth,Codechef,Codeforces etc.. A bot is developed by moghya to scrape solutions from websites and upload to github repo.'
		self.repoName = 'sportProgrammingSubmissionsOf'+self.username
		try:
			self.user = Github(self.username,self.password).get_user()
			self.repo = self.user.get_repo(self.repoName)
			print('Repository already exists.')
		except GithubException as e:
			if e.status==401:
				print('Bad Github Credentials')
				exit()
			elif e.status == 404:
				self.repo = self.user.create_repo(self.repoName,self.repoDesc)
				self.repo.create_file('/README.md','Added README','-This Repository contains my submissions made at multiple sport programming websites.\n -This repository has been created using toGithub app developed by [moghya](https://github.com/moghya/toGithub).')
				self.repo.create_file('/cchef/cchef.txt','Folder Created for Codechef','This Folder Contains Submissions made at Codechef')
				self.repo.create_file('/hrank/hrank.txt','Folder Created for Hackerrank','This Folder Contains Submissions made at Hackerrank')
				self.repo.create_file('/hearth/hearth.txt','Folder Created for Hackerearth','This Folder Contains Submissions made at Hackerearth')
				self.repo.create_file('/cforce/cforce.txt','Folder Created for Codeforces','This Folder Contains Submissions made at Codeforces')

	
	def cchefUpload(self,username,password):
		self.cchefUser = cchef(username,password)
		self.cchefUser.getSubmissions()

	def cforceUpload(self,username,password,offset=1):
		self.cforceUser = cforce(username,password,offset)
		self.cforceUser.getSubmissions()
		for accepted_solution in self.cforceUser.accepted_solutions:
			path = '/cforce/'+accepted_solution['contestId']+'/'+accepted_solution['problemName']+'/'+accepted_solution['id']+'.'+accepted_solution['ext']
			commit = 'cforce submissionId '+accepted_solution['id']+' is added.'
			content = accepted_solution['code']
			self.repo.create_file(path,commit,content)
			print('uploaded '+accepted_solution['contestId']+accepted_solution['problemName'])