# Pagamentos-nibo-api

Automação de pagamentos financeiros via API do Nibo a partir de arquivos PDF.

## Objetivo
- Reduzir trabalho manual do financeiro
- Evitar erros e duplicidade
- Garantir rastreabilidade (logs + evidências)
- Padronizar fluxo: PDF → fornecedor → payload → POST Nibo → arquivo final

## Fluxo (alto nível)

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
  H --> I[Gerar chave de idempotencia]

  I --> J{Pagamento ja processado}
  J -->|Sim| K[Mover PDF para boletos/processados]
  K --> Z

  J -->|Nao| L[POST pagamento API Nibo]
  L --> M{Resposta sucesso}

  M -->|Nao| M1[Registrar erro API]
  M1 --> E2

  M -->|Sim| N[Salvar evidencia pagamento]
  N --> K


