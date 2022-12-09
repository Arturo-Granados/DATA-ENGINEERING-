##########     Setup     ##########
import os 
from twilio.rest import Client
from twilio_config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, coinlayer_api_key, apilayer_api_key
import time 


import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

from datetime import datetime




#Def request_coinlayer function to get data
def request_coinlayer(api_key):
    #Set coinlayer api url
    coinlayer_url = 'http://api.coinlayer.com/live?access_key=' + api_key

    #Try get data with a request method
    try :
        response = requests.get(coinlayer_url).json()
    except Exception as e:
        print('We can not conect')

    return response

#Apply request_coinlayer function 
response_coinlayer = request_coinlayer(coinlayer_api_key)


#Function to create a data set 
def create_dataset(response):
  #Create dataset  
  data = pd.DataFrame(list(response['rates'].items()), columns = ['Coin', 'Prices'])
  #Sort dataset
  data = data.sort_values(by='Prices', ascending=False)
  #Select the first 10 items 
  data = data.head(10)
  return data 

#Apply create_dataset function 
data = create_dataset(response_coinlayer)


#Function to get dolar function 
def request_apilayer(api_key):
  #Set apilayer url
  apilayer_url = "https://api.apilayer.com/exchangerates_data/convert?to=MXN&from=USD&amount=1"
  #Set api key, payload and headers
  api_key = api_key
  payload = {}
  headers= {
  "apikey": api_key
  }
  apilayer_response = requests.request("GET", apilayer_url, headers=headers, data = payload).json()
  #Extract data
  date = apilayer_response['date']
  dolar_value = apilayer_response['result']
  return date, dolar_value

#Apply request_apilayer function 
date, dolar_value = request_apilayer(apilayer_api_key)


#Function to set a message from twilio
def send_message(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,date,dolar_value,data):
  account_sid = TWILIO_ACCOUNT_SID
  auth_token = TWILIO_AUTH_TOKEN

  client = Client(account_sid, auth_token)

  message = client.messages \
      .create(
          from_='whatsapp:+14155238886',
          body='\nHola! \n\n\n El precio de dolar hoy '+ date +' en  Mexico es ' + str(dolar_value) +' pesos.  Y aca el resumen de las cripto \n\n\n ' + str(data),
          to='whatsapp:+5215574608539'
      )

  return message.sid










