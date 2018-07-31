import base64
import hashlib
import os
from Crypto import Random
from Crypto.Cipher import AES

def GenerateKey():
	random_data = os.urandom(128)
	key = hashlib.md5(random_data).hexdigest()[:16]
	key32 = "".join([ ' ' if i >= len(key) else key[i] for i in range(16) ])
	return key32.encode('utf-8')
		

class AESCipher:
    def __init__( self, key):
        self.key = key

    def encrypt( self, raw ):
        BS = 16
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
        raw = pad(raw)
        iv = Random.new().read(BS)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        res = iv + cipher.encrypt( raw )
        return base64.b64encode(res)

def Encrypt(key, raw):
	crypt = AESCipher(key)
	return "{0}".format(crypt.encrypt(raw))
