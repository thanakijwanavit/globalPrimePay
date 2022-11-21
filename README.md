# Global Prime Pay SDK





more info at https://doc.gbprimepay.com
for python docs see https://thanakijwanavit.github.io/globalPrimePay/

## Install

`pip install globalPrimePay`

## How to use

1. Get gbprime secrets
2. `pip install globalPrimePay`
3. python docs [here](https://thanakijwanavit.github.io/globalPrimePay/)

## Secrets

GB prime should give you a password file which should include
> this should also be available at your gbprime console in `profile>show Key` near the bottom of the page

```
public:Public Keysecret: Secret Key
token: Token / Customer Key
```


These key should be saved securely and should never be shared with the client or stored in the source code
We recommend a secret storage service such as `aws secrets manager`
if you are developing your app please use the test domain key

these secrets must be used when initiating the gbp client

# Usage
## Initiate a client 

```
from globalPrimePay.client import Client
client = Client(pub = 'PUBLICKEY', secret='SECRETKEY', token='CLIENT TOKEN')
```

## Pay with credit card

```
sampleCard = {
      "cardNumber": "4535017710535741",
      "expirationMonth": "05",
      "expirationYear": "28",
      "securityCode": "184",
      "name": "Watcharagon Phokonwong"
    }
cardToken = client.getCardToken(**sampleCard)['card']['token']
cardToken
```




    'a76e0bc4-a5ed-4cf1-a6ca-33d185bc7509'



### non-3d payment

```
# non-3d payment
client.chargeCard(
  token = cardToken,
  amount = 100,
  referenceNo = 'ref1',
  customerName = "nic",
  customerEmail = "nicsemail@gmail.com",
  detail =  'test order')
```




    {'customerAddress': None,
     'amount': 100,
     'referenceNo': 'ref1',
     'messageToMerchant': None,
     'resultCode': '00',
     'customerTelephone': None,
     'resultMessage': 'Success',
     'customerName': 'nic',
     'customerEmail': 'nicsemail@gmail.com',
     'gbpReferenceNo': 'gbp173512113574',
     'merchantDefined5': None,
     'detail': 'test order',
     'merchantDefined3': None,
     'merchantDefined4': None,
     'merchantDefined1': None,
     'merchantDefined2': None}



### 3d payment

```
# payment
chargeCardResult = client.chargeCard(
  token = cardToken,
  amount = 100,
  referenceNo = 'ref1',
  customerName = "nic",
  customerEmail = "nicsemail@gmail.com",
  detail =  'test order',
  otp = 'Y'
)
chargeCardResult
```




    {'customerAddress': None,
     'amount': 100,
     'referenceNo': 'ref1',
     'messageToMerchant': None,
     'resultCode': '00',
     'customerTelephone': None,
     'resultMessage': 'Success',
     'customerName': 'nic',
     'customerEmail': 'nicsemail@gmail.com',
     'gbpReferenceNo': 'gbp173512113578',
     'merchantDefined5': None,
     'detail': 'test order',
     'merchantDefined3': None,
     'merchantDefined4': None,
     'merchantDefined1': None,
     'merchantDefined2': None}



### Verify OTP

```
client.verifyOtp(chargeCardResult['gbpReferenceNo'])
```




    '<!DOCTYPE html>\n\n<html>\n  <head>\n    <title>GB Prime Pay</title>\n    <meta charset="UTF-8" />\n    <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n  </head>\n  <body>\n    <div>Loading...</div>\n    <div>\n      <form action="https://simbank.globalprimepay.com/pay/3d_secure" method="post">\n        <input type="hidden" name="MERID" value="21291800058" />\n        <input type="hidden" name="TERMINALID" value="18060001" />\n        <input type="hidden" name="PAN" value="4535017710535741" />\n        <input type="hidden" name="EXPIRYDATE" value="0528" />\n        <input type="hidden" name="CVV2" value="184" />\n        <input type="hidden" name="INVOICENO" value="2209270148" />\n        <input type="hidden" name="AMOUNT" value="10000" />\n        <input type="hidden" name="POSTURL" value="https://api.globalprimepay.com/web/thanachat_gateway/receive/goback" />\n        <input type="hidden" name="POSTURL2" value="https://api.globalprimepay.com/web/thanachat_gateway/receive/realtime" />\n        <input type="hidden" name="AUTOREDIRECT" value="Y" />\n      </form>\n    </div>\n    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>\n    <script type="text/javascript">\n      $(document).ready(function () {\n        $(\'form\').submit();\n      });\n    </script>\n  </body>\n</html>'


