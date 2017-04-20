from scrape.scraper import *
from github import Github


#let's create a class to test Github API and add functions required for upload files etc.
#we'll use already developed wrapper Github

class upToGithub:
	def __init__(self,username,password):
		self.username = username
		self.password = password
		self.user = Github(username,password).get_user()

	def printRepos(self):
		for repo in self.repos:
			print(repo.name)

	def createRepo(self):
		desc = 'This repository contains submissions made on websites like Hackerrank,Hackerearth,Codechef,Codeforces etc.. A bot is developed by moghya to scrape solutions from websites and upload to github repo.'
		repoName = 'sportProgrammingSubmissionsOf'+self.username
		try:
			self.repo = self.user.get_repo(repoName)
			#self.repo.create_file('/cchef/cchef.txt','This Folder Contains Submissions made at Codechef','This Folder Contains Submissions made at Codechef',branch=self.repo._master_branch,committer=self.user,author=self.user)
		except:
			self.repo = self.user.create_repo(repoName,desc)
			pass
		#self.repo.create_file('/cchef/cchef.txt','This Folder Contains Submissions made at Codechef','This Folder Contains Submissions made at Codechef')
		#self.repo.create_file('/hrank/hrank.txt','Folder Created for Hackerrank','This Folder Contains Submissions made at Hackerrank')
		#self.repo.create_file('/hearth/hearth.txt','Folder Created for Hackerearth','This Folder Contains Submissions made at Hackerearth')

	def cchefUpload(self,username,password):
		self.createRepo()
		self.cchefUser = cchef(username,password)
		self.cchefUser.getSubmissions()
		for problemName in self.cchefUser.submissions:
			problem = self.cchefUser.submissions[problemName]
			for solution in problem['submissions']:
				solutionId = solution['id']
				ext = solution['ext']
				code = solution['code']
				print(solutionId)
				self.repo.create_file('/cchef/'+problemName+'/'+solutionId+'.'+ext,'cchef solution for '+problemName+' with solutionId '+solutionId+' is added.',code)