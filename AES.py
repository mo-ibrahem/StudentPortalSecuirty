from Crypto.Cipher import AES
import hashlib

password = b'mypassword'
key = hashlib.sha256(password).digest() # This will automatically give us a 32 byte key

mode = AES.MODE_CBC
IV = b'This is an IV456'

def pad_message(file):
    while len(file)%16 != 0:
        file = file + b'0'
    return file


cypher = AES.new(key,mode,IV)

# Saving encryption key in a text file
with open('EncryptionKey.txt', 'wb') as df:
    df.write(key)

# The message needs to be 32 bytes long
with open ('secret.txt','rb') as f:
    orig_file = f.read()

print("Msg to be encrypted:", orig_file)

padded_file = pad_message(orig_file)

encrypted_file = cypher.encrypt(padded_file)

print("Encrypted Message:",encrypted_file)

with open ('encrypted_secret.txt', 'wb') as e:
    e.write(encrypted_file)

