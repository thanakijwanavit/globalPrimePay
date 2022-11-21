# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/client.ipynb (unless otherwise specified).

__all__ = ['Helper', 'Client', 'getCardToken', 'chargeCard', 'verifyOtp', 'qrPayment', 'checkStatus',
           'PaymentStatusError', 'paymentStatus', 'wechatPay', 'alipay']

# Cell
from nicHelper.wrappers import add_method
from numbers import Number
from typing import Optional
import requests, sentry_sdk, urllib

# Cell
from .helper import Keys, checkSum
from .exceptions import GBPResponseError

# Cell
class Helper:
  @staticmethod
  def urlEncode(params):
    return urllib.parse.urlencode(params)

  successMap = {'G' : 'Generate' , 'A' : 'Authorize' , 'S' : 'Settle', 'V' : 'Void', 'D' : 'Decline'}

# Cell

class Client(Helper):
  '''
    main client for interface with global prime pay
    accept 3 inputs from gbp
    pub: public key
    secret: your secret key
    token: your client token

    please refer to the main readme which should describe what those are
  '''
  def __init__(self, pub, secret, token='', endpoint = 'https://api.globalprimepay.com'):
    '''
      input:
        pub: str:: publiceKey from web
        secret: str:: secretKey from web
      docs (https://doc.gbprimepay.com)
    '''
    self.key = Keys(pub,secret)
    self.endpoint = endpoint
    self.token = token


# Cell
@add_method(Client)
def getCardToken(self, cardNumber, expirationMonth, expirationYear, securityCode, name, **kwargs):

  body = {
    "rememberCard": True,
    "card": {
      "number": cardNumber,
      "expirationMonth": expirationMonth,
      "expirationYear": expirationYear,
      "securityCode": securityCode,
      "name": name
    }
    ,**kwargs
  }

  headersCharge = {
    'Authorization': self.key.pubPL,
    'Content-Type': 'application/json',
  }
  baseURL = self.endpoint
  url = f'{baseURL}/v2/tokens'
  r:requests.Response = requests.post(url,headers = headersCharge, json = body)
  jsonResponse = r.json()
  if r.status_code >= 400:
    sentry_sdk.add_breadcrumb(category = 'gbPrimePay', data = {'input':body, 'response':jsonResponse} , level = 'critical')
    raise GBPResponseError(f'error response, input payload is {body}, response from gb is {jsonResponse}')
  return jsonResponse


# Cell
@add_method(Client)
def chargeCard(self, token:str,
               amount:Number,
               referenceNo:str,
               customerName:str,
               customerEmail:str,
               detail:str,
               responseUrl:str = "https://responseUrl",
               backgroundUrl:str =  "https://backgroundUrl",
               otp:str = "Y",
               **kwargs)->dict:
  '''
    charge card using 3d security,
    input:
      token:str:: card token (generated using client.getCardToken
      amount:Number:: amount to charge
      referenceNo:str:: reference used to check payment status later, should be uniquely generated
      customerName:str
      customerEmail:str
      detail:str
      responseUrl:str:: redirect url
      backgroundUrl:str:: callback url
      otp:str:: should we force user to input OTP 'Y' or 'N'
      **kwargs: any other input, please see full reference here https://doc.gbprimepay.com/full-payment-3d
  '''
  body = {
    "amount": amount,
    "referenceNo": referenceNo,
    "detail": detail,
    "customerName": customerName,
    "customerEmail": customerEmail,
    "card": {
      "token": token
    },
    "otp": otp,
    "responseUrl": responseUrl,
    "backgroundUrl": backgroundUrl,
    **kwargs
  }

  url = f'{self.endpoint}/v2/tokens/charge'
  headers = {
    'Authorization': self.key.secPL,
    'Content-Type': 'application/json',
  }
  r = requests.post(url, json=body, headers = headers)
  jsonResponse = r.json()
  # handle error
  if r.status_code >= 400:
    sentry_sdk.add_breadcrumb(category = 'gbPrimePay', data = {'input':body, 'response':jsonResponse} , level = 'critical')
    raise GBPResponseError(f'error response, input payload is {body}, response from gb is {jsonResponse}')
  return jsonResponse



# Cell
@add_method(Client)
def verifyOtp(self, gbpReferenceNo):
  params = {
      'publicKey': self.key.pub,
      'gbpReferenceNo': gbpReferenceNo
  }
  headers3d = {
    'Content-Type': 'application/x-www-form-urlencoded',
  }
  url = self.endpoint + "/v2/tokens/3d_secured"
  r = requests.post(url, params=params, headers = headers3d)
  if r.status_code >= 400:
    sentry_sdk.add_breadcrumb(category = 'gbPrimePay', data = {'input':params, 'response':r.text} , level = 'critical')
    raise GBPResponseError(f'error response, input payload is {params}, response from gb is {r.text}')
  return r.text

# Cell
@add_method(Client)
def qrPayment(self, amount:Number, referenceNo:str, *args, **kwargs):
  '''
    pass through variable except token is get from the main class, please see docs at
    https://doc.gbprimepay.com/qrcash
    currently only amount and referenceNo are required
  '''
  url = f'{self.endpoint}/v3/qrcode/text'
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
  }
  body = {
    'token': self.token,
    'amount': amount,
    'referenceNo': referenceNo,
    **kwargs
  }
  r = requests.post(url, data = self.urlEncode(body), headers = headers)
  return r.json()


# Cell
@add_method(Client)
def checkStatus(self, referenceNo, **kwargs):
  url = f'{self.endpoint}/v1/check_status_txn'
  headers = {
    'content-type': 'application/json',
    'Authorization': self.key.secPL
  }
  body = {'referenceNo': referenceNo }
  r:requests.Response = requests.post(url, headers=headers, json = body)
  if r.status_code >=400: raise Exception(f'error checking status {r.text}')
  return r.json()

# Cell
class PaymentStatusError(Exception): pass

@add_method(Client)
def paymentStatus(self, referenceNo, **kwargs):
  try:
    status =  self.checkStatus(referenceNo).get('txn',None)['status'] or self.checkStatus(referenceNo).get('txns',None)[0]['status']
    print('status is', self.successMap[status])
    return status
  except Exception as e:
    print(self.checkStatus(referenceNo))
    print('error', e)
    raise PaymentStatusError(e)

# Cell
@add_method(Client)
def wechatPay(self, amount:Number, referenceNo:str, *args, **kwargs):
  '''
    pass through variable except token is get from the main class, please see docs at
    https://doc.gbprimepay.com/wechat
    currently only amount and referenceNo are required
  '''
  url = f'{self.endpoint}v3/wechat/text'
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
  }
  body = {
    'token': self.token,
    'amount': amount,
    'referenceNo': referenceNo,
    **kwargs
  }
  r = requests.post(url, data = self.urlEncode(body), headers = headers)
  return r.json()


# Cell
@add_method(Client)
def alipay(self, amount:Number, referenceNo:str, *args, **kwargs):
  '''
    pass through variable except token is get from the main class, please see docs at
    https://doc.gbprimepay.com/wechat
    currently only amount and referenceNo are required
  '''
  url = f'{self.endpoint}v2/alipay'
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
  }
  body = {
    'token': self.token,
    'amount': amount,
    'referenceNo': referenceNo,
    **kwargs
  }
  r = requests.post(url, data = self.urlEncode(body), headers = headers)
  return r.text
