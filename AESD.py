from Crypto.Cipher import AES
import hashlib

password = b'mypassword'
# key = hashlib.sha256(password).digest() # This will automatically give us a 32 byte key
with open('EncryptionKey.txt', 'rb') as e:
    key = e.read()

mode = AES.MODE_CBC
IV = b'This is an IV456'

cipher = AES.new(key,mode,IV)

with open('encryptetCloud.txt', 'rb') as e:
    encrypted_file = e.read()

print("Encrypted File:", encrypted_file)
decrypted_file = cipher.decrypt(eval(encrypted_file))

with open('decrypted_secret.txt', 'wb') as df:
    df.write(decrypted_file.rstrip(b'0'))

print("Decrypred File: ",decrypted_file)