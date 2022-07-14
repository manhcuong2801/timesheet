import base64

# secret_key = "Bd8=ks56qplMz9@3"
secret_key = "Zjz9Eq7Pj.n7kbUX"
#
# key = base64.b64encode(secret_key.encode("ascii"))
# plain_text = '1090149601'
plain_text = "2fAhJdWWimqTc3YrIz7MCjUoq78TFXL"
# plain_text = base64.b64encode(plain_text.encode("utf-8"))
# # cipher = AES.new(key, AES.MODE_ECB)
# # ciphertext, tag = cipher.encrypt(plain_text)
# # return ciphertext, tag
# cipher = AES.new(key, AES.MODE_ECB)
# msg = cipher.encrypt(plain_text)
# print(base64.b64decode(msg).decode())

from binascii import b2a_hex, a2b_hex

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def decode_base64_to_string(raw_text):
    return base64.b64encode(raw_text).decode()


def encode_string_to_base64(raw_text):
    base64_bytes = raw_text.encode("utf-8")
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.hex()


def encrypt(raw):
    raw = pad(raw.encode(), 16)
    cipher = AES.new(secret_key.encode("utf-8"), AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(raw))


msg = encrypt("hao　hao")
msg_str = decode_base64_to_string(msg)

msg_encoded = encode_string_to_base64(msg_str)


def decrypt(encrypted_text):
    enc = base64.b64decode(encrypted_text)
    cipher = AES.new(secret_key.encode("utf-8"), AES.MODE_ECB)
    return unpad(cipher.decrypt(enc), 16).decode("utf-8")


msg2 = decrypt(msg_str)
print(f"zzz: {msg2}")
