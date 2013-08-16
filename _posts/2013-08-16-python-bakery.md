---
categories: 
  - post
published: false
layout: default
---


```python
key = "privatekey"

  data = request.cookies.get('CHOCOLATECHIP')
  flash(data)
  if data:
    data = urllib.unquote(data.encode('ascii')).decode("utf-8")
    data = base64.b64decode(data)

    signature = data[0:64]
    encrypted_data = data[64:]

    token = hmac.new(key, encrypted_data, hashlib.sha256).hexdigest()

    if signature == token:
      from Crypto.Cipher import AES
      
      mode = AES.MODE_ECB
      padded_key = key.ljust(16, '\0')
      decryptor = AES.new(padded_key, mode)
      from phpserialize import loads
      cchip =  loads(decryptor.decrypt(encrypted_data))
      
```
      