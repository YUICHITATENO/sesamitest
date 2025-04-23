# test_unlock.py
import requests
import time
from Crypto.Hash import CMAC
from Crypto.Cipher import AES

# === あなたのセサミデバイス情報 ===
device_id = '112004200708042468004900ffffffff'  # ハイフンなしのUUID
secret_key = bytes.fromhex('77a9edef9f831ddb3313a2c805247b7a')  # 署名キー
api_key = 'M13mLsBXOo4nQMkB0T4Gt5hze6iuJV4I8RA1feGc'  # APIキー
cmd = 83  # 83=unlock, 82=lock, 88=toggle
history = 'manual-test'  # 操作履歴として表示される文字

# === タイムスタンプ生成 ===
timestamp = int(time.time())
ts_bytes = timestamp.to_bytes(4, byteorder='little')

# === 署名メッセージ作成 ===
message = bytes.fromhex(device_id) + ts_bytes + bytes([cmd])
cmac = CMAC.new(secret_key, ciphermod=AES)
cmac.update(message)
sign = cmac.hexdigest()

# === セサミAPIへリクエスト ===
url = f'https://app.candyhouse.co/api/sesame2/{device_id}/cmd'
headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json'
}
payload = {
    'cmd': cmd,
    'history': history,
    'sign': sign
}

print('🔐 Sending request to Sesame API...')
response = requests.post(url, json=payload, headers=headers)
print('✅ Response code:', response.status_code)
print('📬 Response body:', response.text)
