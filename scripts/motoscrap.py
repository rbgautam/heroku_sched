from lxml import html
import requests
# from twilio.rest import Client
from time import sleep
import sys
from threading import Timer
from datetime import datetime
import os


def read_html():
    try:
        # page = requests.get('https://ce.harpercollege.edu/public/category/programArea.do?method=load&selectedProgramAreaId=29362')
        page = requests.get('https://ce.harpercollege.edu/search/publicCourseAdvancedSearch.do?method=doPaginatedSearch&showInternal=false&cspIndex=true&isPageDisplayed=true&courseSearch.courseDescriptionKeyword=LMT&courseSearch.disciplineCode=&courseSearch.partialCourseNumber=&courseSearch.courseCategoryStringArray=0&courseSearch.sectionSemesterIdString=&courseSearch.sectionInstructorName=&courseSearch.sectionAccreditingAssociationStringArray=0&courseSearch.sectionDayOfWeekStringArray=0&courseSearch.sectionStartTimeStringArray=0&courseSearch.sectionStartMonthStringArray=0&courseSearch.filterString=availforreg')
        tree = html.fromstring(page.content)
        
        data_strong_html = tree.xpath('//*[@id="programAreaDescription"]/h3[1]/b/strong/text()')
        # print(data_strong_html[0])
        data_text_html = tree.xpath('//*[@id="courseSearchResult"]/tbody/tr/td[1]/span[1]/a/text()')
        # print(data_text_html[0])
        assert_text = data_text_html[0]
        assert_text2 = tree.xpath('//*[@id="courseSearchResult"]/tbody/tr/td[4]/span/text()')[0]
        # print(assert_text2)
        if 'Motorcycle' in assert_text and assert_text2 != 'Full':
            send_sms()
            rt.stop()
            sys.exit("Course open")
            quit()

        else:
            now = datetime.now()
            current_time = now.strftime("%D %H:%M:%S")
            print('Search Page: text match at '+ current_time)
            read_html2()
    except Exception as ex:
        send_sms()
        print(ex)

def read_html2():
    page = requests.get('https://ce.harpercollege.edu/public/category/programArea.do?method=load&selectedProgramAreaId=29362')
    tree = html.fromstring(page.content)
    
    data_strong_html = tree.xpath('//*[@id="programAreaDescription"]/h3[1]/b/strong/text()')
    # print(data_strong_html[0])
    # data_text_html = tree.xpath('//*[@id="variableContentBlockPG0035"]/div/text()')
    # # print(data_text_html[0])
    assert_text = data_strong_html[0]
    if assert_text == '04/17/2022':
        now = datetime.now()
        current_time = now.strftime("%D %H:%M:%S")
        print('Main Page: text match at '+ current_time)
    else:
        send_sms()
        rt.stop()
        sys.exit("Course open")
        quit()
def read_rom_html(page):
    base_url = 'https://www.consoleroms.com/roms/gbc'
    page = requests.get('https://www.consoleroms.com/roms/gbc/page/'+str(page))
    tree = html.fromstring(page.content)
    
    data_strong_html = tree.xpath('//*[@class="imgCon"]/a/@href')
    for i in range(0,15):
        full_url = base_url + data_strong_html[i]+ '/download'
        print(full_url)
def get_page_data():
    for i in range(1,32):
         read_rom_html(i) 

def send_sms():
    try:
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)

        message = client.messages.create(
         body='Course open again \n https://ce.harpercollege.edu/search/publicCourseAdvancedSearch.do?method=doPaginatedSearch&showInternal=false&cspIndex=true&isPageDisplayed=true&courseSearch.courseDescriptionKeyword=LMT&courseSearch.disciplineCode=&courseSearch.partialCourseNumber=&courseSearch.courseCategoryStringArray=0&courseSearch.sectionSemesterIdString=&courseSearch.sectionInstructorName=&courseSearch.sectionAccreditingAssociationStringArray=0&courseSearch.sectionDayOfWeekStringArray=0&courseSearch.sectionStartTimeStringArray=0&courseSearch.sectionStartMonthStringArray=0&courseSearch.filterString=availforreg',
         from_=os.environ['TWILIO_FROM_NUMBER'],
         to=os.environ['TWILIO_TO_NUMBER1'])
        message = client.messages.create(
         body='Course open again \n https://ce.harpercollege.edu/search/publicCourseAdvancedSearch.do?method=doPaginatedSearch&showInternal=false&cspIndex=true&isPageDisplayed=true&courseSearch.courseDescriptionKeyword=LMT&courseSearch.disciplineCode=&courseSearch.partialCourseNumber=&courseSearch.courseCategoryStringArray=0&courseSearch.sectionSemesterIdString=&courseSearch.sectionInstructorName=&courseSearch.sectionAccreditingAssociationStringArray=0&courseSearch.sectionDayOfWeekStringArray=0&courseSearch.sectionStartTimeStringArray=0&courseSearch.sectionStartMonthStringArray=0&courseSearch.filterString=availforreg',
         from_=os.environ['TWILIO_FROM_NUMBER'],
         to=os.environ['TWILIO_TO_NUMBER2'])
        print(message.sid)
    except Exception as ex:
        print(ex)


def request_validation_in_intervals():
    global rt
    rt = RepeatedTimer(300, read_html) # it auto-starts, no need of rt.start()
    
    try:
        sleep(10000) # your long-running job goes here...
    finally:
        rt.stop() # better in a try/finally block to make sure the program ends!

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
        print('Stopping execution ')
        quit()

# 
# send_mail()
# send_sms()
# read_html()
#get_page_data()
request_validation_in_intervals()
