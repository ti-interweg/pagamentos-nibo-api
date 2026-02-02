# src/payload_builder.py
from datetime import datetime

def br_to_iso(d: str) -> str:
    # "01/02/2026" -> "2026-02-01"
    return datetime.strptime(d, "%d/%m/%Y").date().isoformat()

def parse_valor(valor_str: str) -> float:
    # "120,00" -> 120.00
    v = (valor_str or "").strip().replace(".", "").replace(",", ".")
    return float(v)

def build_debit_payload(*, stakeholder_id: str, boleto: dict, defaults: dict, reference: str) -> dict:
    valor = parse_valor(boleto["valor_str"])
    venc = br_to_iso(boleto["vencimento"])

    category_id = defaults.get("categoryId")
    cost_center_id = defaults.get("costCenterId")
    ccv_type = defaults.get("costCenterValueType", 1)

    payload = {
        "stakeholderId": stakeholder_id,
        "description": boleto.get("cedente") or "Pagamento fornecedor",
        "reference": reference,
        "scheduleDate": venc,
        "dueDate": venc,
        "accrualDate": venc,
        "categories": [
            {"categoryId": category_id, "value": valor}
        ],
        "costCenterValueType": ccv_type,
        "costCenters": [
            {"costCenterId": cost_center_id, "percent": 100}
        ],
        # se seu endpoint exigir "instalment"/"installment", a gente ativa depois.
    }
    return payload