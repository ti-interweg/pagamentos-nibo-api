import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("NIBO_API_TOKEN")
if not token:
    raise RuntimeError("NIBO_API_TOKEN não encontrado no .env")

url = "https://api.nibo.com.br/empresas/v1/stakeholders"

resp = requests.get(
    url,
    params={"$top": 500},
    headers={
        "ApiToken": token,
        "Accept": "application/json"
    },
    timeout=60
)

resp.raise_for_status()

items = resp.json().get("items", [])
suppliers = [x for x in items if x.get("type") == "Supplier"]

print(f"Total de stakeholders: {len(items)}")
print(f"Total de suppliers: {len(suppliers)}\n")

for s in suppliers[:30]:
    print(f"- {s.get('name')}  | id={s.get('id')}")