# Pagamentos Nibo API

Automação do processamento de pagamentos financeiros via **API do Nibo**, a partir de **arquivos PDF de boletos**, com foco em segurança, rastreabilidade e eliminação de trabalho manual no financeiro.

---

## Visão Geral

Este projeto implementa um fluxo automatizado para:

- Ler PDFs de boletos recebidos
- Extrair dados financeiros relevantes
- Resolver o fornecedor no Nibo
- Montar o payload conforme contrato da API
- Enviar o pagamento via POST
- Garantir idempotência (sem duplicidade)
- Organizar arquivos e registrar evidências

O sistema foi projetado para uso interno, com governança, documentação e preparo para auditoria.

---

## Fluxograma (alto nível)

```mermaid
flowchart TD
  A[Inicio: PDF chega na pasta boletos/entrada] --> B{Detectar PDFs novos}

  B -->|Nenhum| Z[Fim]
  B -->|Encontrou| C[Mover PDF para boletos/processando]

  C --> D[Extrair dados do PDF]
  D --> E{Dados obrigatorios OK}

  E -->|Nao| E1[Registrar erro]
  E1 --> E2[Mover PDF para boletos/erro]
  E2 --> Z

  E -->|Sim| F[Resolver fornecedor stakeholderId]
  F --> G{Fornecedor encontrado}

  G -->|Nao| G1[Registrar erro ou pendencia]
  G1 --> E2

  G -->|Sim| H[Montar payload pagamento]
  H --> I[Gerar chave idempotencia]

  I --> J{Pagamento ja processado}
  J -->|Sim| K[Mover PDF para boletos/processados]
  K --> Z

  J -->|Nao| L[POST pagamento API Nibo]
  L --> M{Resposta sucesso}

  M -->|Nao| M1[Registrar erro API]
  M1 --> E2

  M -->|Sim| N[Salvar evidencia pagamento]
  N --> K

ESTRUTURA DO PROJETO

finance-bots/
├─ boletos/
│  ├─ entrada/        PDFs recebidos
│  ├─ processando/    PDFs em processamento
│  ├─ processados/    PDFs concluídos com sucesso ou duplicidade
│  └─ erro/           PDFs com erro e evidência
│
├─ src/
│  ├─ pipeline.py             Orquestração do fluxo
│  ├─ idempotency.py          Controle de duplicidade
│  ├─ payload_builder.py      Montagem do payload para API do Nibo
│  ├─ stakeholder_resolver.py Resolução de fornecedor
│  ├─ nibo_client.py          Cliente HTTP da API do Nibo
│  └─ list_suppliers.py       Consulta de fornecedores
│
├─ docs/              Documentação funcional e técnica
├─ app.py             Entry point da aplicação
├─ config.yaml        Configurações gerais
├─ requirements.txt   Dependências Python
├─ .env.example       Exemplo de variáveis de ambiente
└─ README.md

Pré-requisitos
Python 3.10 ou superior / Git / Token válido da API do Nibo

Instalação

python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

Configuração

NIBO_BASE_URL=https://api.nibo.com.br
NIBO_TOKEN=SEU_TOKEN_REAL
NIBO_COMPANY_ID=ID_DA_EMPRESA

Execução

python app.py


Pasta docs/

docs/
├─ 01-visao-geral.md
├─ 02-contrato-dados.md
├─ 03-regras-negocio.md
└─ 04-erros-e-excecoes.md




