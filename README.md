# Global Prime Pay SDK





more info at https://doc.gbprimepay.com
for python docs see https://thanakijwanavit.github.io/globalPrimePay/

## Install

`pip install globalPrimePay`

## How to use

1. Get appropriate secret and public key
2. go through get started
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
