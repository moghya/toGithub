from toGithub.scrapeSubmissions import hearth
from github import Github


#let's create a class to test Github API and add functions required for upload files etc. 
#we'll use already developed wrapper PyGithub

class upToGithub:
	def __init__(self,username,password):
		self.user = Github(username,password)
		self.repos = self.user.get_user().get_repos()

	def printRepos(self):
		for repo in self.repos:
			print(repo.name)


def test_upToGithub():
	user = upToGithub('moghya','helpit70.')
	user.printRepos()
	#hearth.test_hearth()

test_upToGithub()