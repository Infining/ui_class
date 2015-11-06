import re

import requests
from bs4 import BeautifulSoup


class course:
    def __init__(self,year,semester,school,course):
        self.error = 0

        if (semester == 'Fall'):
            num_semester = 10
        elif (semester == 'Spring'):
            num_semester = 20

        # Parse full url
        url_base = 'http://webpages.uidaho.edu/schedule/'
        url_full = url_base + str(year) + str(num_semester) + school + '.htm'

        # Retrieve html from url
        session = requests.session()
        req     = session.get(url_full)
        doc     = BeautifulSoup(req.content, "html.parser")

        # Find the first course section that matches given specifications
        header        = "T3"
        currentClass  = doc.find("td", {"headers" : header})
        course_search = re.search("<b>(.*)</b>", str(currentClass.contents))
        course_search = int(course_search.group(1))

        while course_search != course:
            currentClass = currentClass.findNext("td", {"headers" : header})
            if currentClass == None:
                self.error = 'could not find class'
                break
            course_search = re.search("<b>(.*)</b>", str(currentClass.contents))
            course_search = int(course_search.group(1))

        self.course_index = []
        index        = 0
        nextSection  = currentClass

        # Determine total number of course sections and compile them into the matrix self.course_index
        while course_search == course:
            self.course_index.append([])
            self.course_index[index].append(nextSection)
            nextSection = self.course_index[index][0].findNext("td", {"headers" : header})
            if nextSection == None: # Check for end of page
                break
            course_search = re.search("<b>(.*)</b>", str(nextSection.contents))
            course_search = int(course_search.group(1))
            index += 1

        index = 0
        for section in self.course_index:
            classSection = section[0]
            self.course_index[index].append(self.courseCRN(classSection))
            self.course_index[index].append(self.courseNUM(classSection))
            self.course_index[index].append(self.courseSEC(classSection))
            self.course_index[index].append(self.courseCRED(classSection))
            self.course_index[index].append(self.courseTITLE(classSection))
            self.course_index[index].append(self.courseSDATE(classSection))
            self.course_index[index].append(self.courseEDATE(classSection))
            self.course_index[index].append(self.courseSTIME(classSection))
            self.course_index[index].append(self.courseETIME(classSection))
            index += 1

        # need to check and handle multiple sections and class times

    # end of __init__

    def courseCRN(self, currentClass):
        header  = "T1"
        td      = currentClass.findPrevious("td", {"headers" : header})
        content = re.search("<b>(.*)</b>", str(td.contents))
        crn     = int(content.group(1))
        return crn

    def courseNUM(self, currentClass):
        header  = "T3"
        td      = currentClass.findPrevious("td", {"headers" : header})
        content = re.search("<b>(.*)</b>", str(td.contents))
        crn     = int(content.group(1))

    def courseSEC(self, currentClass):
        header  = "T4"
        td      = currentClass.findNext("td", {"headers" : header})
        content = re.search("<i>(.*)</i>", str(td.contents))
        sec     = int(content.group(1))
        return sec

    def courseCRED(self, currentClass):
        header  = "T5"
        td      = currentClass.findNext("td", {"headers" : header})
        content = re.search("<i>(.*)</i>", str(td.contents))
        cred    = int(content.group(1))
        return cred

    def courseTITLE(self, currentClass):
        header  = "T6"
        td      = currentClass.findNext("td", {"headers" : header})
        content = re.search("<i>(.*)</i>", str(td.contents))
        title   = str(content.group(1))
        return title

    def courseSDATE(self, currentClass):
        header  = "T8"
        td      = currentClass.findNext("td", {"headers" : header})
        content = re.search("\\\\n(.*)\\\\xa0", str(td.contents))
        sdate   = str(content.group(1))
        return sdate

    def courseEDATE(self, currentClass):
        header  = "T9"
        td      = currentClass.findNext("td", {"headers" : header})
        content = re.search("\\\\n(.*)\\\\xa0", str(td.contents))
        edate   = str(content.group(1))
        return edate

    def courseSTIME(self, currentClass):
        header = "T10"
        td = currentClass.findNext("td", {"headers" : header})
        content = re.search("\\\\n(.*) -", str(td.contents))
        if content == None:
            content = re.search("\\\\n(.*)\\\\xa0", str(td.contents))
            stime = str(content.group(1))
            return stime
        stime = str(content.group(1))
        if stime.find('am') != -1:
            stime_h = re.search("(.*):", stime)
            stime_m = re.search(":(.*) ", stime)
            stime   = int(str(stime_h.group(1)) + str(stime_m.group(1)))
        elif stime.find('pm') != -1:
            stime_h = re.search("(.*):", stime)
            stime_m = re.search(":(.*) ", stime)
            stime   = int(str(stime_h.group(1)) + str(stime_m.group(1)))
            if stime < 1200:
                stime = etime + 1200
        return stime

    def courseETIME(self, currentClass):
        header = "T10"
        td = currentClass.findNext("td", {"headers" : header})
        content = re.search("- (.*)\\\\xa0", str(td.contents))
        if content == None:
            content = re.search("\\\\n(.*)\\\\xa0", str(td.contents))
            stime = str(content.group(1))
            return stime
        stime = str(content.group(1))
        if stime.find('am') != -1:
            stime_h = re.search("(.*):", stime)
            stime_m = re.search(":(.*) ", stime)
            stime   = int(str(stime_h.group(1)) + str(stime_m.group(1)))
        elif stime.find('pm') != -1:
            stime_h = re.search("(.*):", stime)
            stime_m = re.search(":(.*) ", stime)
            stime   = int(str(stime_h.group(1)) + str(stime_m.group(1)))
            if stime < 1200:
                stime = etime + 1200
        return stime

course = course(2015,'Spring','ECE',444)
title  = course.course_index
for section in title:
    for atrib in section[1:]:
        print(atrib)
    print("-------------")
