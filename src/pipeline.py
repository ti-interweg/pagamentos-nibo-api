# src/pipeline.py
import os
from pathlib import Path
from datetime import datetime

from src.stakeholder_resolver import find_supplier_stakeholder_id
from src.payload_builder import build_debit_payload

def process_folder(cfg: dict, token: str, bradesco_code: str, nibo_code: str):
    entrada = Path(cfg["paths"]["entrada"])
    proc = Path(cfg["paths"]["processados"])
    erro = Path(cfg["paths"]["erro"])

    entrada.mkdir(parents=True, exist_ok=True)
    proc.mkdir(parents=True, exist_ok=True)
    erro.mkdir(parents=True, exist_ok=True)

    # carrega stakeholders UMA vez
    nibo = cfg["_nibo_client"]
    st_data = nibo.list_stakeholders(top=3000)
    stakeholders = st_data.get("items", [])

    defaults = cfg.get("defaults", {})

    for file in entrada.iterdir():
        if not file.is_file():
            continue
        if file.suffix.lower() != ".pdf":
            continue

        try:
            stakeholder_id = find_supplier_stakeholder_id(
                stakeholders,
                cnpj=boleto.get("cnpj"),
                name=boleto.get("cedente"),
            )

            if not stakeholder_id:
                raise RuntimeError(
                    f"Fornecedor não encontrado no Nibo (Supplier). "
                    f"cedente='{boleto.get('cedente')}', cnpj='{boleto.get('cnpj')}'"
                )

            reference = f"{bradesco_code}-{nibo_code}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

            payload = build_debit_payload(
                stakeholder_id=stakeholder_id,
                boleto=boleto,
                defaults=defaults,
                reference=reference,
            )

            nibo.create_payable(payload)

            # move para processados
            dest = proc / file.name
            file.replace(dest)

        except Exception as e:
            # move para erro + grava log
            dest = erro / file.name
            try:
                file.replace(dest)
            except Exception:
                pass

            err_path = erro / f"{file.name}.err.txt"
            err_path.write_text(str(e), encoding="utf-8")