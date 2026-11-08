from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent
for item in json.loads((P/'manifest.json').read_text()):
 f=P/item['file'];assert hashlib.sha256(f.read_bytes()).hexdigest()==item['sha256']
 response=json.loads(f.read_text())['response']
 for token in item['required_substantive_tokens']:assert token in response,(f.name,token)
 assert 'Content type:' in response
print('PASS: successful rendered captures hashed and substantive metadata present; no microdata asserted')
