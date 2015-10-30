import requests
import BeautifulSoup
import re

def find_course(year,semester,school,course):
    """

    """

    if (semester == 'Fall'):
        num_semester = 10
    elif (semester == 'Spring'):
        num_semester = 20

    url_base = 'http://webpages.uidaho.edu/schedule/'
    url_full = url_base + str(year) + str(num_semester) + school + '.htm'

    session = requests.session()
    req = session.get(url_full)
    doc = BeautifulSoup.BeautifulSoup(req.content)

    # Find course number on page
    header ="T3"
    currentClass = doc.find("td", {"headers" : header})
    course_search = re.search("<b>(.*)</b>", str(currentClass.contents))
    course_search = int(course_search.group(1))

    while course_search != course:
        currentClass = currentClass.findNext("td", {"headers" : header})
        course_search = re.search("<b>(.*)</b>", str(currentClass.contents))
        course_search = int(course_search.group(1))

    # Class CRN
    header = "T1"
    td = currentClass.findPrevious("td", {"headers" : header})
    content = re.search("<b>(.*)</b>", str(td.contents))
    crn = int(content.group(1))

    # Class section
    header = "T4"
    td = currentClass.findNext("td", {"headers" : header})
    content = re.search("<i>(.*)</i>", str(td.contents))
    sec = int(content.group(1))

    # Class credits
    header = "T5"
    td = currentClass.findNext("td", {"headers" : header})
    content = re.search("<i>(.*)</i>", str(td.contents))
    cred = int(content.group(1))

    # Class title
    header = "T6"
    td = currentClass.findNext("td", {"headers" : header})
    content = re.search("<i>(.*)</i>", str(td.contents))
    title = str(content.group(1))

    # Class start date
    header = "T8"
    td = currentClass.findNext("td", {"headers" : header})
    content = re.search("n(.*)&nbsp;", str(td.contents))
    sdate = str(content.group(1))

    # Class end date
    header = "T9"
    td = currentClass.findNext("td", {"headers" : header})
    content = re.search("n(.*)&nbsp;", str(td.contents))
    edate = str(content.group(1))

    # Class start time
    header = "T10"
    td = currentClass.findNext("td", {"headers" : header})
    print str(td.contents)
    content = re.search("n(.*) -", str(td.contents))
    stime = str(content.group(1))
    if stime.find('am') != -1:
        stime_h = re.search("(.*):", stime)
        stime_m = re.search(":(.*) ", stime)
        stime = int(str(stime_h.group(1)) + str(stime_m.group(1)))
        print stime
    elif stime.find('pm') != -1:
        stime_h = re.search("(.*):", stime)
        stime_m = re.search(":(.*) ", stime)
        stime = int(str(stime_h.group(1)) + str(stime_m.group(1)))
        if stime < 1200:
            stime = etime + 1200

    # Class start time
    header = "T10"
    td = currentClass.findNext("td", {"headers" : header})
    print str(td.contents)
    content = re.search("- (.*)&nbsp;", str(td.contents))
    etime = str(content.group(1))
    if etime.find('am') != -1:
        etime_h = re.search("(.*):", etime)
        etime_m = re.search(":(.*) ", etime)
        etime = int(str(etime_h.group(1)) + str(etime_m.group(1)))
        print etime
    elif etime.find('pm') != -1:
        etime_h = re.search("(.*):", etime)
        etime_m = re.search(":(.*) ", etime)
        etime = int(str(etime_h.group(1)) + str(etime_m.group(1)))
        if etime < 1200:
            etime = etime + 1200
        print etime

    classArray = [crn,course_search,sec,cred,title,sdate,edate,stime,etime]
    print classArray


find_course(2015,'Spring','ECE',240)
