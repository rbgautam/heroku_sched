from lxml import html
import requests
from twilio.rest import Client
from time import sleep
import sys
from threading import Timer
from datetime import datetime
import os
import interval_timer

base_url = 'https://finance.yahoo.com/quote/'
symbols = json.loads(os.environ['STOCK_DICT'])

def get_stock_data():
    for item in symbols.keys():
        read_html(item)


def read_html(symbol):
    try:
        formed_url = base_url+symbol;
        page = requests.get(formed_url)
        tree = html.fromstring(page.content)
        # print(tree)

        data_symbol_price_html = tree.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span/text()')
        
        stock_price = float(data_symbol_price_html[0])
        # print(stock_price)
        curr_profit = ((stock_price - symbols[symbol])/symbols[symbol])*100
        now = datetime.now()
        current_time = now.strftime("%D %H:%M:%S")
        txtMsg = current_time + " Current stock_price for {0}, Price= {1}, profit = {2}".format(symbol,stock_price,curr_profit)
        if curr_profit > 20:
            send_sms(txtMsg)
            
        else:
            now = datetime.now()
            current_time = now.strftime("%D %H:%M:%S")
            txtMsg = current_time + " Current stock_price for {0}, Price= {1}, profit = {2}".format(symbol,stock_price,curr_profit)
            print(txtMsg)
          
    except Exception as ex:
        # send_sms()
        print(ex)



def send_sms(msg):
    try:
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)

        message = client.messages.create(
         body=msg,
         from_=os.environ['TWILIO_FROM_NUMBER'],
         to=os.environ['TWILIO_TO_NUMBER1'])
       
        print(message.sid)
    except Exception as ex:
        print(ex)


def request_validation_in_intervals():
    global rt
    rt = interval_timer.RepeatedTimer(5, get_stock_data) # it auto-starts, no need of rt.start()
    
    try:
        sleep(10000) # your long-running job goes here...
    finally:
        rt.stop() # better in a try/finally block to make sure the program ends!



# get_stock_data()
request_validation_in_intervals()