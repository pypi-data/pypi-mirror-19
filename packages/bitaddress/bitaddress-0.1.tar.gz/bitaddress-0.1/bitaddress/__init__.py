import ctypes
import hashlib
from ecdsa import SigningKey, SECP256k1
from .base58 import encode as base58_encode

def get_key():
	return SigningKey.generate(curve=SECP256k1)

def get_coordinates(key):
	return key.get_verifying_key().pubkey.point.x(), key.get_verifying_key().pubkey.point.y()

def generate_address(k=get_key, version=0):
	if callable(k):
		k = k()

	x,y = get_coordinates(k)
	s=b'\x04' + bytes(str(x), encoding='utf8') + bytes(str(y), encoding='utf8')

	hasher = hashlib.sha256()
	hasher.update(s)
	r=hasher.digest()

	hasher = hashlib.new('ripemd160')
	hasher.update(r)
	r = hasher.digest()

	if version == 0:
		return '1'+base58_check(r, version=version)
	return base58_check(r, version=version)

def base58_check(src, version=0):
	src = bytes([version])+src
	hasher=hashlib.sha256()
	hasher.update(src)
	r=hasher.digest()

	hasher=hashlib.sha256()
	hasher.update(r)
	r=hasher.digest()

	checksum=r[:4]
	s=src+checksum

	return base58_encode(int.from_bytes(s, 'big'))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='Generate a bitcoin address')
	parser.add_argument('version', help='Use another version byte', type=int, metavar='V', const=0, nargs='?', default=0)

	args = parser.parse_args()

	key = get_key()
	print('ADDRESS: ' + generate_address(k=get_key(), version=args.version))
	ptiny('PRIVATE KEY: ' + base58_check(k.privkey))