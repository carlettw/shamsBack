"""Supabase Storage ulanishini tekshiradi (.env dagi qiymatlar bilan).

Ishga tushirish:  python test_storage.py
Kalitning o'zini ekranga chiqarmaydi.
"""
import base64
import json

import requests

from app.core.config import settings

url = (settings.SUPABASE_URL or "").rstrip("/")
key = (settings.SUPABASE_SERVICE_ROLE_KEY or "").strip()
bucket = settings.SUPABASE_STORAGE_BUCKET

print("SUPABASE_URL           :", url or "(BO'SH)")
print("Bucket                 :", bucket)
print("Kalit uzunligi         :", len(key), "belgi (oddiy service_role ~219)")
print("Kalit .. bilan boshlanadi:", key[:8] or "(BO'SH)")

try:
    payload = key.split(".")[1]
    payload += "=" * (-len(payload) % 4)
    claims = json.loads(base64.urlsafe_b64decode(payload))
    print("Kalit loyihasi (ref)   :", claims.get("ref"), "| rol:", claims.get("role"))
    host_ref = url.replace("https://", "").split(".")[0]
    print("URL va kalit mos mi    :", "HA" if claims.get("ref") == host_ref else "YO'Q  <-- shu sabab!")
except Exception as e:
    print("Kalit JWT emas yoki buzilgan:", e)

if not url or not key:
    raise SystemExit("\nSUPABASE_URL yoki kalit .env dan o'qilmadi.")

h = {"apikey": key, "Authorization": f"Bearer {key}"}
r = requests.get(f"{url}/storage/v1/bucket", headers=h, timeout=20)
print("\nBucketlar ro'yxati     :", r.status_code, r.text[:200])

up = requests.post(
    f"{url}/storage/v1/object/{bucket}/_test/ping.txt",
    headers={**h, "Content-Type": "text/plain", "x-upsert": "true"},
    data=b"ok",
    timeout=20,
)
print("Test fayl yuklash      :", up.status_code, up.text[:200])
if up.status_code == 200:
    print("\nHAMMASI ISHLAYAPTI: kalit va bucket to'g'ri.")
