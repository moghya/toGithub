from scrape.scraper import *
from upload.uploader import *


def test_cchef():
	user = cchef('cchefUsername','cchefPassword.')
	user.getSubmissions()

def test_upToGithub():
	user = upToGithub('githubUsername','githubPassword')
	user.cchefUpload('cchefUsername','cchefPassword.')

test_upToGithub()
