from build import *
# Reuse the original acquisition; refresh requires a separate archive directory.
f=P/'fallback_manifest.json'
if not f.is_file(): raise SystemExit('Missing archive manifest; acquire into a new directory.')
rec=json.loads(f.read_text())
if 'path' in rec:
 raw=P/rec['path']
 if not raw.is_file() or hashlib.sha256(raw.read_bytes()).hexdigest()!=rec['sha256']:
  raise SystemExit(f'Archive missing or SHA-256 mismatch: {raw}')
print('Verified archived MODIS response; no network requests made.')
