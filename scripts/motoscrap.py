from lxml import html
import requests
from twilio.rest import Client
from time import sleep
import sys
from threading import Timer
from datetime import datetime



def read_html():
    page = requests.get('https://ce.harpercollege.edu/public/category/programArea.do?method=load&selectedProgramAreaId=29362')
    tree = html.fromstring(page.content)
    
    data_strong_html = tree.xpath('//*[@id="programAreaDescription"]/h3[1]/b/strong/text()')
    # print(data_strong_html[0])
    data_text_html = tree.xpath('//*[@id="programAreaDescription"]/h3[1]/b/text()')
    # print(data_text_html[0])
    if data_strong_html[0] == '04/23/2021':
        
        now = datetime.now()
        current_time = now.strftime("%D %H:%M:%S")
        print('text match at '+ current_time)
    else:
        send_sms()


def send_sms():
    try:
        account_sid = 'AC810644ffe834065bc01effa922457941' #os.environ['TWILIO_ACCOUNT_SID']
        auth_token = '4ff2e4899e889007c5932da3ba193eb3'#os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)

        message = client.messages.create(
         body='Course open again \n https://ce.harpercollege.edu/public/category/programArea.do?method=load&selectedProgramAreaId=29362',
         from_='+13027867257',
         to='+16412260994')
        message = client.messages.create(
         body='Course open again \n https://ce.harpercollege.edu/public/category/programArea.do?method=load&selectedProgramAreaId=29362',
         from_='+13027867257',
         to='+13125327290')
        print(message.sid)
    except Exception as ex:
        print(ex)


def request_validation_in_intervals():
    global rt
    rt = RepeatedTimer(10, read_html) # it auto-starts, no need of rt.start()
    
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
request_validation_in_intervals()