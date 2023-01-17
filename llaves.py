from Crypto.PublicKey import RSA

key = RSA.generate(1024)
pub_key = key.public_key().export_key("PEM")
priv_key = key.export_key("PEM")

with open("public_key", 'wb') as f:
    f.write(pub_key)
with open("private_key", 'wb') as f:
    f.write(priv_key)
