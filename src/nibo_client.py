# src/nibo_client.py
import requests

class NiboClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.s = requests.Session()
        self.s.headers.update({
            "ApiToken": token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def create_payable(self, payload: dict) -> dict:
        url = f"{self.base_url}/empresas/v1/schedules/debit"
        r = self.s.post(url, json=payload, timeout=60)

        # se der erro, levanta com corpo (p/ debug)
        if not r.ok:
            raise RuntimeError(f"HTTP {r.status_code} - {r.text}")

        # nem sempre vem JSON
        try:
            return r.json()
        except Exception:
            return {"status_code": r.status_code, "text": r.text}

    def list_stakeholders(self, top: int = 2000) -> dict:
        url = f"{self.base_url}/empresas/v1/stakeholders"
        r = self.s.get(url, params={"$top": str(top)}, timeout=60)
        if not r.ok:
            raise RuntimeError(f"HTTP {r.status_code} - {r.text}")
        return r.json()