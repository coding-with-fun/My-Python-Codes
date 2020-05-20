import hashlib, binascii

crypt = hashlib.sha384()

crypt.update(b"Hello")

print("sha384 encypted text is: " + crypt.hexdigest())
print("Size of sha384 encypted text is: " + str(crypt.digest_size))

cryptText = hashlib.pbkdf2_hmac('sha256', b'hello', b'abc', 1000000)

print("PKCS#5 password-based key derivation is: " + str(binascii.hexlify(cryptText)))
