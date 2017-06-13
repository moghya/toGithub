import json as j
from scrape.scraper import *
from upload.uploader import *
def test_upToGithub():
	user = upToGithub('moghya','helpit70.')
	user.cforceUpload('sawant','helpit70.')

def initialization():
	try:
		with open('userData.json') as user_data_file:
			userData = j.load(user_data_file)
			if userData['github_username']!='' and userData['github_password']!='':
				if (userData['codechef_username']!='' and userData['codechef_password']!='') or (userData['codeforces_username']!='' and userData['codeforces_password']!=''):
					return userData
				else:
					print('Configure userData.json and set credentials for Codechef or Codeforces Account. Thanks')
					return None
			else:
				print('Configure userData.json and set credentials for Github Account. Thanks')
				return None
	except:
		print('Hello bud, It seems that you haven\'t configured userData.json file or there\'s some error. \n Please configure it and execute this later. Thanks.')
		return None

<<<<<<< HEAD
def saveData(userData):
	f = open('userData.json','w')
	f.write(j.dumps(userData,indent=4))
	f.close()

def main():
	userData = initialization()
	if userData is not None:
		toGithubUser = upToGithub(userData['github_username'],userData['github_password'])
		if userData['codeforces_username']!='' and userData['codeforces_password']!='':
			print(userData['codeforces_offset'])
			print(userData['codeforces_username']+', I\'m scraping codeforces for you.')
			toGithubUser.cforceUpload(userData['codeforces_username'],userData['codeforces_password'],userData['codeforces_offset'])
			userData['codeforces_offset'] = toGithubUser.cforceUser.offset
			print(userData['codeforces_offset'])
		userData['codechef_username'] = 'hurr'
		saveData(userData)
	else:
		print('Aborting....')
		return

=======
def test_cchef():
	user = cchef('cchefUsername','cchefPassword.')
	user.getSubmissions()

def test_upToGithub():
	user = upToGithub('githubUsername','githubPassword')
	user.cchefUpload('cchefUsername','cchefPassword.')
>>>>>>> origin/master

if __name__ == '__main__':
	main()