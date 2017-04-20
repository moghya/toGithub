from scrape.scraper import *
from upload.uploader import *


def test_cchef():
	user = cchef('moghya','helpit70.')
	user.getSubmissions()

def test_upToGithub():
	user = upToGithub('moghya','helpit70.')
	user.cchefUpload('moghya','helpit70.')

test_upToGithub()
