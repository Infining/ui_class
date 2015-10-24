import requests
import BeautifulSoup

# Need to check for compatable version of python

url_base = 'http://webpages.uidaho.edu/schedule/'

year = input('Enter the year (2014, 2015, ect.): ')

# 'raw_input' is required for inputing strings in 2.7.*, is not required for python 3.*
semester = raw_input('Enter the semester (Fall or Spring): ')

school = raw_input('Enter the School that your class is in (ACCT, AERO, AG, ect.): ')

crn = input('Enter class CRN: ')

if (semester == 'Fall'):
    num_semester = 10
elif (semseter == 'Spring'):
    num_semester = 20

url_full = url_base + str(year) + str(num_semester) + school + '.htm'

print url_full

session = requests.session()

req = session.get(url_full)

doc = BeautifulSoup.BeautifulSoup(req.content)

print doc.findAll('a', {"class" : "gp-share"})
