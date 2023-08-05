import requests
from Crypto import Random
import hashlib
from Crypto.Cipher import AES
import base64

salt = "1789F0B8C4A051E5"

def send(key, title, message, event=None):
    if not key or not message:
        raise ValueError("Key and message argument must be set")

    payload = {"key" : key, "msg" : message}

    if title:
        payload.update({"title" : title})

    if event:
        payload.update({"event" : event})

    requests.post('https://api.simplepush.io/send', data = payload)

def send_encrypted(key, password, title, message, event=None):
    encryption_key = generate_encryption_key(password)
    iv = Random.new().read(AES.block_size)
    iv_hex = "".join("{:02x}".format(ord(c)) for c in iv).upper()
    iv_byte_str = str(bytearray.fromhex(iv_hex))

    payload = {"key" : key, "encrypted" : "true", "iv" : iv_hex}

    if title:
        title = encrypt(encryption_key, iv, title)
        payload.update({"title" : title})

    if event:
        payload.update({"event" : event})

    message = encrypt(encryption_key, iv, message)
    payload.update({"msg" : message})

    requests.post('https://api.simplepush.io/send', data = payload)

def generate_encryption_key(password):
    hex_str = hashlib.sha1(password + salt).hexdigest()[0:32]
    byte_str = str(bytearray.fromhex(hex_str))
    return byte_str

def encrypt(encryption_key, iv, data):
    BS = 16
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 

    data = pad(data)

    encrypted_data = AES.new(encryption_key, AES.MODE_CBC, IV=iv).encrypt(data)
    return base64.urlsafe_b64encode(encrypted_data)
