# src/idempotency.py
import re
import hashlib

def br_money_to_float(s: str) -> float:
    # "7.571,58" -> 7571.58
    s = s.replace(".", "").replace(",", ".")
    return float(s)

def make_reference(boleto: dict) -> str:
    valor = int(round(br_money_to_float(boleto["valor_str"]) * 100))
    venc = boleto["vencimento"].replace("/", "")
    if boleto.get("linha_digitavel"):
        base = boleto["linha_digitavel"]
        return f"BOL-{base[-10:]}-{venc}-{valor}"  # curto e auditável
    cnpj = boleto.get("cnpj") or "SEM-CNPJ"
    nosso = boleto.get("nosso_numero") or "SEM-NOSSO"
    return f"BOL-{cnpj}-{nosso}-{venc}-{valor}"

def make_unique_key(boleto: dict) -> str:
    ref = make_reference(boleto)
    return hashlib.sha1(ref.encode("utf-8")).hexdigest()