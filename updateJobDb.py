from more_itertools import unique_everseen
from requests.auth import HTTPBasicAuth
from flashtext import KeywordProcessor
from time import gmtime, strftime
import jobDbHandler as db
import scrape as scraper
import requests
import string
import base64
import time
import json
import re

### Script to manage Jobs DB. Run every 10 minutes ###

start = time.time() ##Start timer
allJobs = []
jobCats = ['computer%20science', 'python developer', 'javascript developer', 'c%23 developer', 'c%2B%2B developer', 'c developer', 'linux', 'server developer', 'developer', 'windows server', 'linux server', 'Sql Developer', 'PHP Developer', 'programming', ' cloud engineer', '.net developer', 'server engineer', 'Google Cloud Platform', 'Java developer', 'DevOps', 'Unix Developer', 'Software Engineer']
keyword_dict = { ##Keywords for search
    "Python":['python', 'Python', 'python3', 'python2', 'pip'],
    "C++":["c++", 'c++ developer', 'c++ engineer', 'c++ DevOps'],
    "JavaScript":['javascript', 'javascript developer', 'nodejs', 'node-js', 'js'],
    "C#":['C#', 'C Sharp', 'Csharp', 'Microsoft C#'],
    "Linux":['linux', 'ubuntu', 'arch', 'debian', 'unix'],
    "Unix":['unix', 'linux'],
    "Teaching":['teacher', 'teaching', 'teach'],
    "Junior":['junior'],
    "DevOps":['DevOps'],
    "Windows server":['Windows Server'],
    "Windows":['Windows', 'windows'],
    "Apple":['MacOs', 'IOS', 'Swift', 'Macbook', 'apple'],
    "SQL":['SQL', 'Sequel', 'MongoDB', 'SQLite', 'Mysql', 'oracle'],
    "Google Cloud Platform":['Google Cloud Platform'],
    "AWS":['AWS', 'Amazon Web Service'],
    "Flask":['flask', 'Flask'],
    "Django":['django'],
    "Software Engineer":['Software Engineer'],
    "Audio":['audio'],
    "Go Lang":['golang', 'go lang'],
    "Senior":['senior'],
    "AI":['Artificial Intelligence', 'AI'],
    "Ruby":['ruby', 'rubyonrails'],
    "HTML":['html', 'css'],
    "CSS":['css', 'html'],
    "Node-js":['nodejs', 'node-js', 'node js'],
    "React-js":['React', 'react'],
    "Full Stack":['Full Stack', 'full stack'],
    "Documentation":['documentation'],
    "Automation":['automation', 'Automation'],
    "Developer":['Developer', 'developing'],
    "Engineer":['Engineer', 'engineer'],
    "IT":['IT', 'Information Technology'],
    "Support":['Support', 'Phone'],
    "Java":['Java', 'java'],
    "VMware":['VMWare'],
    "Infrastructure":['Infrastructure'],
    "System Admin":['Sysadmin', 'System Admin', 'System Administrator'],
    "Trainee":['Trainee'],
    "ASP.net":['ASP.net'],
    "Excel":['excel'],
    "Bootstrap":['bootstrap'],
    "Laravel":['Laravel'],
    "Moodle":['moodle'],
    "Wordpress":['wordpress'],
    "Mid-level":['Mid-level', 'midlevel', 'mid level'],
    "SaaS":['SaaS'],
    "Analytics":['Analytics'],
    "Azure":['Azure'],
    "Google Cloud":['Google Cloud'],
    "Security":['Security'],
    "Blockchain":['Blockchain', 'Bitcoin'],
    "Kotlin":['Kotlin'],
    "Android":['Android']
}
keyword_processer = KeywordProcessor()
keyword_processer.add_keywords_from_dict(keyword_dict)

def deEmojify(text): ##Removes emoji's and other unicode
    printable = set(string.printable)
    return ''.join(filter(lambda x: x in printable, text))

def getJobs(searchTerm): ##Function to get json from jobCats
    response = requests.get('https://www.reed.co.uk/api/1.0/search?keywords={}'.format(searchTerm), auth = HTTPBasicAuth('23a78aa5-3cab-446a-b925-3134520fe1a3', ''))
    for i in range(0,99):
        try:
            allJobs.append(json.loads(response.text)['results'][i]) 
        except:
            break

def removeOldJobs(oldJobs):
    o = []
    counter2 = 0
    for i in db.retrieve():
        o.append(i[5])
    for i in o:
        if strftime("/%m/", gmtime()) in i and int(strftime("%d", gmtime())) >= int(i[:2]):
            print("Deleting {}".format(oldJobs[12]))
            db.deleteRow(oldJobs[12])
            counter2 = counter2 + 1
    return counter2

for i in jobCats:
    getJobs(i)

allJobs = list(unique_everseen(allJobs)) ##Removes duplicates
oJobs = db.retrieveOldUrl()
oldJobs = []
for i in oJobs:
    oldJobs.append(i[0])
allOldJobs = db.retrieve()
aOJ = []
for i in allOldJobs:
    aOJ.append(i)
counter2 = removeOldJobs(aOJ[12])
counter = 0
for i in allJobs: ##Checks for new jobs and runs them
    if i['jobUrl'] in oldJobs:
        print('already exists')
        continue
    else:
        if strftime("/%m/", gmtime()) in i['date'] and int(i['date'][:2]) < int(strftime("%d", gmtime())):
            isNew = False
        else:
            isNew = True
        counter = counter + 1
        company = i['employerName']
        companyLogoUrl = scraper.getPfp(i['jobUrl'])
        timePosted = i['date']
        timeExpired = i['expirationDate']
        if i['minimumSalary'] != None:
            salary = str("£"+str(i['minimumSalary'])+'-'+str(i['maximumSalary']))
        else:
            salary = 'N/A'
        location = i["locationName"]
        preDescription = i["jobDescription"]
        fullDescription = str(scraper.getDescription(i['jobUrl'])[9:])
        keywords = keyword_processer.extract_keywords(i['jobTitle'])
        keywords = list(unique_everseen(keywords))
        applications = str(i['applications'])
        jobUrl = str(i['jobUrl'])
        title = str(i['jobTitle'])
        db.insertNewJob(deEmojify(title), isNew, deEmojify(company), companyLogoUrl, timePosted, timeExpired, salary, deEmojify(location), deEmojify(preDescription), deEmojify(fullDescription), json.dumps(keywords), applications, jobUrl)
        print("[Done]"+title+"\n")
end = time.time() ##End timer

print('[Finished] added {} jobs, removed {} jobs.\n[Time Taken] {}s'.format(counter, counter2, str(int(end)-int(start))))
with open("logs/updateJobDb.log", "w") as f:
    f.write("[{}] added {} jobs, removed {} jobs.\n[Time Taken] {}s\n\n".format(strftime("%d/%m/%Y %H:%M:%S", gmtime()), counter, counter2, str(int(end)-int(start))))