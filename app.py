# app.py
import os
import argparse
import yaml
from pathlib import Path
from dotenv import load_dotenv

from src.nibo_client import NiboClient
from src.pipeline import process_folder

def main():
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("--bradesco", required=True)  # ex: A
    parser.add_argument("--nibo", required=True)      # ex: N1
    args = parser.parse_args()

    ROOT_DIR = Path(__file__).resolve().parent
    config_path = ROOT_DIR / "config.yaml"

    with open(config_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    token_env = cfg["nibo"]["token_env"]
    token = os.getenv(token_env)
    if not token:
        raise RuntimeError(f"Faltou env {token_env} no .env")

    base_url = cfg["nibo"]["base_url"]
    nibo = NiboClient(base_url=base_url, token=token)
    cfg["_nibo_client"] = nibo

    process_folder(cfg, args.bradesco, args.nibo)

if __name__ == "__main__":
    main()