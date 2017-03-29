import json
import requests
from bs4 import BeautifulSoup

#step 1 lets create class to get solutions from hearth

class hearth:

    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.accepted_submissions = []
        self.session = requests.Session()
        self.login()

    def login(self):
        url = 'https://www.hackerearth.com/'
        response = self.session.get(url)
        request_cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(self.session.cookies))
        request_headers = {
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, sdch, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Connection':'keep-alive',
            'Host':'www.hackerearth.com',
            'Referer':url,
            'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
        }
        request_data = {
            'login':self.username,
            'password':self.password,
            'next':'/users/basic-details/'
        }
        ajax_url = 'https://www.hackerearth.com/AJAX/login/'
        self.session.post(ajax_url,data=request_data,headers=request_headers,cookies=request_cookies)

    def get_solutions(self):
        problems = {

        }
        url = 'https://www.hackerearth.com/submissions/{}/'.format(self.username)
        response = self.session.get(url)
        request_cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(self.session.cookies))
        request_headers = {
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, sdch, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Connection':'keep-alive',
            'Host':'www.hackerearth.com',
            'Referer':url,
            'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
        }
        ajax_url = 'https://www.hackerearth.com/AJAX/feed/newsfeed/submission/user/{}/?result=AC'.format(self.username)
        repeat = True
        while repeat:
            response = self.session.get(ajax_url,headers=request_headers,cookies=request_cookies)
            json_response = json.loads(response.text)
            parsed_reponse = BeautifulSoup(str(json_response['data']),'lxml')
            trs = parsed_reponse.find('table').findAll('tr')
            for i in range(1,len(trs)):
                tr = trs[i]
                tds = tr.findAll('td')
                problem = tds[1].find('a')
                problem_link = problem['href']
                problem_slug = problem_link.split('/')[-2]
                if problem_slug not in problems:
                    problems[problem_slug] = {}
                    problem_name = str(problem.text).strip(' \n \n ')
                    lang = str(tds[5].text).strip(' \n \n ')
                    submission_code = str(tds[6].find('a')['href']).split('/')[-2]
                    problems[problem_slug]['problem_link'] = problem_link
                    problems[problem_slug]['submission_code'] = submission_code
                    problems[problem_slug]['problem_name'] = problem_name
                    problems[problem_slug]['lang'] = lang
            page = parsed_reponse.find('span',{'class':'step-links'}).findAll('a')[-1]
            if page.has_attr('data-gotopage'):
                repeat = True
                page = page['data-gotopage']
                ajax_url = 'https://www.hackerearth.com/AJAX/feed/newsfeed/submission/user/{}/?result=AC&page={}'.format(self.username,page)
            else:
                repeat = False

        self.accepted_submissions = problems
        print(json.dumps(problems,indent=4))


user = hearth('moghya','helpit70.')
user.get_solutions()