import json
import codecs
import requests
from bs4 import BeautifulSoup

#step 1 lets create class to get solutions from cchef
extensions = {
    'ADA':'',
    'ASM':'',
    'BASH':'sh',
    'BF':'',
    'C':'c',
    'C99 strict':'',
    'CAML':'',
    'CLOJ':'',
    'CLPS':'',
    'CPP 4.3.2':'cpp',
    'CPP 4.9.2':'cpp',
    'C++14':'cpp',
    'CS2':'',
    'D':'',
    'ERL':'',
    'FORT':'',
    'FS':'',
    'GO':'',
    'HASK':'',
    'ICK':'',
    'ICON':'',
    'JAVA':'java',
    'JS':'js',
    'LISP clisp':'',
    'LISP sbcl':'',
    'LUA':'',
    'NEM':'',
    'NICE':'',
    'NODEJS':'',
    'PAS fpc':'',
    'PAS gpc':'',
    'PERL':'',
    'PERL6':'',
    'PHP':'php',
    'PIKE':'',
    'PRLG':'',
    'PYPY':'',
    'PYTH':'py',
    'PYTH 3.4':'py',
    'RUBY':'',
    'SCALA':'',
    'SCM chicken':'',
    'SCM guile':'',
    'SCM qobi':'',
    'ST':'',
    'TCL':'tcl',
    'TEXT':'',
    'WSPC':'',
    'C++11':'cpp',
    'GNU C':'c',
    'GNU C11':'c',
    'GNU C++':'cpp',
    'GNU C++11':'cpp',
    'GNU C++14':'cpp',
    'MS C++':'',
    'MONO C#':'',
    'MS C#':'',
    'D':'',
    'Go':'',
    'Haskell':'',
    'Java 8':'java',
    'Kotlin':'',
    'Ocaml':'',
    'Delphi':'',
    'FPC':'',
    'Perl':'',
    'PHP':'php',
    'Python 2':'py',
    'Python 3':'py',
    'PyPy 2':'',
    'PyPy 3':'',
    'Ruby':'rb',
    'Rust':'',
    'Scala':'',
    'JavaScript':'js'
}



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
                print(uid)
                problem['submissions_link'] = p.find('a')['href']
                problem['submissions'] = []
                response = self.session.get('https://www.codechef.com'+problem['submissions_link']+'?status=15')
                parsed_response = BeautifulSoup(response.text,'lxml')
                for s in parsed_response.find('tbody').findAll('tr'):
                    submission = {}
                    tds = s.findAll('td')
                    submission['id'] = tds[0].text
                    print('\t\t'+submission['id'])
                    submission['lang'] = tds[-2].text
                    submission['ext'] = 'txt'
                    if submission['lang'] in extensions:
                        submission['ext'] = extensions[submission['lang']]
                    submission['link'] = tds[-1].find('a')['href']
                    self.session.headers = {
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Encoding':'gzip, deflate, sdch, br',
                        'Accept-Language':'en-US,en;q=0.8',
                        'Connection':'keep-alive',
                        'Cookie':'_hjIncludedInSample=1; poll_time=1492695114844; notification=0; SESS6e579b771ca1747c067c1551742708ad=09db97cc6e5699f5c6b3ee06535b8bfd; __utmt=1; __asc=df2e6cf215b8b8fe49c49e8984b; __auc=b288342e157376f26b19b410a82; __utma=100380940.203442932.1474435759.1492664051.1492695035.182; __utmb=100380940.7.10.1492695035; __utmc=100380940; __utmz=100380940.1492409091.180.22.utmcsr=homebar|utmccn=sd17|utmcmd=banner',
                        'Host':'www.codechef.com',
                        'Upgrade-Insecure-Requests':'1'
                    }
                    response = self.session.get('https://www.codechef.com'+submission['link'])
                    parsed_response = BeautifulSoup(response.text,'lxml')
                    submission['code'] = ''
                    try:
                        for li in parsed_response.find('div',{'id':'solutiondiv'}).find('ol').findAll('li'):
                            submission['code']+= li.text.strip('\n') +'\n'
                    except:
                        print('Except occurred')
                        pass
                    problem['submissions'].append(submission)
                self.submissions[uid]=problem

#step 2 lets create class to get solutions from hearth
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
                    problems[problem_slug]['problem_link'] = problem_link
                    problems[problem_slug]['submissions'] = []
                    problems[problem_slug]['problem_name'] = problem_name
                submission_code = tds[6].find('a')['href']
                if submission_code:
                    lang = str(tds[5].text).strip(' \n \n ')
                    submission_code= str(submission_code).split('/')[-2]
                    submission = {}
                    submission['lang'] = lang
                    submission['code'] =submission_code
                    problems[problem_slug]['submissions'].append(submission)

            page = parsed_reponse.find('span',{'class':'step-links'}).findAll('a')[-1]
            if page.has_attr('data-gotopage'):
                repeat = True
                page = page['data-gotopage']
                ajax_url = 'https://www.hackerearth.com/AJAX/feed/newsfeed/submission/user/{}/?result=AC&page={}'.format(self.username,page)
            else:
                repeat = False

        self.accepted_submissions = problems
        print(json.dumps(problems,indent=4))


#######################################################
#step 3 lets create class to get solutions from hrank #
#this is broken, we need to fix this
#
#
#######################################################

class hrank:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.accepted_solutions = []


    def get_solutions(self):
        session = requests.Session()


#class for codeforces.com and it works in pretty good way.
class cforce:

    def __init__(self,username,password,offset):
        self.username = username
        self.password = password
        self.session  = requests.Session()
        self.accepted_solutions = []
        self.offset = offset

    def getSubmissions(self):
        response = json.loads(self.session.get('http://codeforces.com/api/user.status?handle='+self.username+'&from=1').text)
        print(response['status']+' now got codeforces submisions.')
        data = {
            'csrf_token':BeautifulSoup(self.session.get('http://codeforces.com/submissions/'+self.username).text,'lxml').find('meta',{'name':'X-Csrf-Token'})['content']
        }
        for result in response['result']:
            if result['id']<=self.offset:
                break
            print(result['verdict'])
            if result['verdict']=='OK':
                submission = {}
                submission['id'] = str(result['id'])
                submission['lang'] = result['programmingLanguage']
                submission['ext'] = 'txt'
                if submission['lang'] in extensions:
                    submission['ext']=extensions[submission['lang']]
                else:
                    print('Don\'t have Extension for '+submission['lang']+' using .txt')
                submission['contestId'] = str(result['problem']['contestId'])
                submission['problemName'] = result['problem']['index']
                data['submissionId'] = submission['id']
                submissionResponse = json.loads(self.session.post('http://codeforces.com/data/submitSource',data=data).text)
                submission['code'] = submissionResponse['source']
                print('scraped '+submission['contestId']+submission['problemName'])
                self.accepted_solutions.append(submission)
        if len(response['result'])>0:
            self.offset = response['result'][0]['id']