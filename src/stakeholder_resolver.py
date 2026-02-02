import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

NIBO_URL = "https://api.nibo.com.br/empresas/v1/stakeholders"
TOKEN = (os.getenv("NIBO_API_TOKEN") or "").strip()

if not TOKEN:
    raise RuntimeError("NIBO_API_TOKEN não encontrado no .env")

HEADERS = {
    "ApiToken": TOKEN,
    "Accept": "application/json"
}

def normalize(text: str) -> str:
    if not text:
        return ""
    text = text.upper()
    # mantém letras/números/espaço
    text = re.sub(r"[^A-Z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def digits_only(s: str) -> str:
    return re.sub(r"\D", "", s or "")

def get_all_suppliers(limit: int = 500) -> list[dict]:
    r = requests.get(
        NIBO_URL,
        params={"$top": str(limit)},   # ✅ Nibo usa $top
        headers=HEADERS,
        timeout=60
    )
    r.raise_for_status()
    items = r.json().get("items", [])
    return [x for x in items if x.get("type") == "Supplier" and not x.get("isDeleted")]

def resolve_stakeholder_id(cedente: str, cnpj: str | None = None) -> str:
    suppliers = get_all_suppliers()

    ced_norm = normalize(cedente)
    cnpj_digits = digits_only(cnpj)

    # 1) tenta por CNPJ (mais confiável)
    if cnpj_digits:
        for s in suppliers:
            doc = s.get("document", {}) or {}
            doc_num = digits_only(doc.get("number", ""))
            if doc_num and doc_num == cnpj_digits:
                return s["id"]

    # 2) tenta por nome (contains)
    for s in suppliers:
        if ced_norm and ced_norm in normalize(s.get("name", "")):
            return s["id"]

    # 3) fallback: match por palavras-chave (p/ casos de abreviação)
    ced_words = [w for w in ced_norm.split() if len(w) >= 3]
    best = None
    best_score = 0

    for s in suppliers:
        name_norm = normalize(s.get("name", ""))
        score = sum(1 for w in ced_words if w in name_norm)
        if score > best_score:
            best_score = score
            best = s

    # exige pelo menos 2 palavras batendo (ajustável)
    if best and best_score >= 2:
        return best["id"]

    raise RuntimeError(
        "Fornecedor não encontrado no Nibo (Supplier). "
        f"cedente='{cedente}', cnpj='{cnpj}'"
    )