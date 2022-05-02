# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/helper.ipynb (unless otherwise specified).

__all__ = ['Keys']

# Cell
import base64

# Cell

class Keys:

  def __init__(self, pub, secret, **kwargs):
    '''
    a key payload generator for global prime pay
    inputs:
      pub: str:: gpp public key from console
      secret: str:: gpp secret key from console
    '''
    self.pub = pub
    self.sec = secret
  @property
  def secPL(self):
    return self.keyPayload(self.sec + ":")
  @property
  def pubPL(self):
    return self.keyPayload(self.pub + ":")


  @staticmethod
  def keyPayload(key:str):
      return f'Basic {base64.b64encode(key.encode()).decode()}'