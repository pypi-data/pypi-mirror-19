# coding=utf-8
import os
from Crypto.PublicKey import RSA
from pyasn1.codec.der import decoder as der_decoder
from pyasn1.codec.der import encoder as der_encoder
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from passlib.hash import pbkdf2_sha1, pbkdf2_sha512
import binascii
from base64 import b64encode

id_seed_cbc = (1, 2, 410, 200004, 1, 4)
id_seed_cbc_with_sha1 = (1, 2, 410, 200004, 1, 15)

#class 시작

class hannpki:
	
	def __int__(self):
		pass
	def load_pubkey_online(self,data):
		self.data= der_decoder.decode(data)[0][0][6][1]
		self.pub_data = self.bit2string(self.data)
		self.start = '-----BEGIN PUBLIC KEY-----'
		self.end = '-----END PUBLIC KEY-----'
		self.public_key = self.start+'\n'+b64encode(self.pub_data)+'\n'+self.end
		return self.public_key

	def load_pubkey(self, pub_path=None):
		self.pub_path = pub_path
		self.check = self.check_file(self.pub_path)
		if self.check == 1:
			raise ValueError( "dose not exist %s file"%(str(self.pub_path)))
	
		if self.check == 2:
			raise ValueError( "dose not aceess %s file"%(str(self.pub_path)))

		p = open(self.pub_path,'rb').read()
		data= der_decoder.decode(p)[0][0][6][1]
		self.pub_data = self.bit2string(data)
		self.start = '-----BEGIN PUBLIC KEY-----'
		self.end = '-----END PUBLIC KEY-----'
		self.public_key = self.start+'\n'+b64encode(self.pub_data)+'\n'+self.end
		return self.public_key

	def load_prikey(self, pri_path=None, passwd=None):
		self.pri_path = pri_path
		self.check = self.check_file(self.pri_path)
		
		if self.check == 1:
			raise ValueError( "dose not exist %s file"%(str(self.pri_path)))
	
		if self.check == 2:
			raise ValueError( "dose not aceess %s file"%(str(self.pri_path)))

		if passwd==None:
			raise ValueError( "need %s file password"%(str(self.pri_path)))

		p = open(self.pri_path,'rb').read()
		data = der_decoder.decode(p)[0]
		algorithm_type = data[0][1][1][0].asTuple()

		if algorithm_type not in (id_seed_cbc_with_sha1, id_seed_cbc):
			raise ValueError( "unKnown algorithm_type")

		if algorithm_type == id_seed_cbc:

			self.salt = data[0][1][0][1][0].asOctets()
			self.iv = data[0][1][1][1].asOctets()
			self.iter_cnt = int(data[0][1][0][1][1])
			self.passwd = passwd
			self.ciphertext = data[1].asOctets()
			self.dk = pbkdf2_sha1.encrypt(self.passwd, salt = self.salt, salt_size = 40, rounds = self.iter_cnt)
			self.dk = binascii.b2a_hex(binascii.a2b_base64(self.dk.split('$')[-1] + "=")).decode()
			self.k = self.dk[:32].decode('hex')
			self.decrypdata = self.seed_cbc_128_decrypt(self.k,self.ciphertext,self.iv)
			self.der_pri = der_decoder.decode(self.decrypdata)
        		self.der_pri2 = str(self.der_pri[0][2]).encode('hex')
			self.der_pri3 = b64encode(self.der_pri2.decode('hex'))
			self.start='-----BEGIN PRIVATE KEY-----'
			self.end='-----END PRIVATE KEY-----'
			self.rsa_pri = self.start+'\n'+self.der_pri3+'\n'+self.end
			return self.rsa_pri
	
		

		elif algorithm_type == id_seed_cbc_with_sha1 :
			raise ValueError( "Sorry %s type not support"%(str(id_seed_cbc_with_sha1)))




		
	def seed_cbc_128_decrypt(self,key, ciphertext, iv):
		    '''general function - decrypt ciphertext with seed-cbc-128(key, iv)'''
		    self.backend = default_backend()
		    self.cipher = Cipher(algorithms.SEED(key), modes.CBC(iv), backend=self.backend)
		    self.decryptor = self.cipher.decryptor()
		    self.decrypted_text = self.decryptor.update(ciphertext)
		    self.unpadder = padding.PKCS7(128).unpadder()
		    self.unpadded_text = self.unpadder.update(self.decrypted_text) + self.unpadder.finalize()
		    return self.unpadded_text

	
	def bit2string(self,data):
		    self.bits = list(data) + [0] * ((8 - len(data) % 8) % 8)
		    self.blist = []
		    for i in range(0, len(self.bits), 8):
			self.blist.append(chr(int(''.join(str(b) for b in self.bits[i:i + 8]), 2)))
		    self.data = ''.join(self.blist)
		    return self.data

	def check_file(self, filename=None):
		self.filename = filename

		if not os.path.isfile(self.filename):
			return 1

		if not os.access(self.filename,os.R_OK):
			return 2
