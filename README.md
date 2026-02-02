# pagamentos-nibo-api

Automação de pagamentos financeiros via API do Nibo a partir de arquivos PDF.

## Objetivo
- Reduzir trabalho manual do financeiro
- Evitar erros e duplicidade
- Garantir rastreabilidade (logs + evidências)
- Padronizar fluxo: PDF → fornecedor → payload → POST Nibo → arquivo final

## Fluxo (alto nível)

```mermaid
flowchart TD
  A[Início: PDF chega na pasta /boletos/entrada] --> B{Detectar PDFs novos}
  B -->|Nenhum| Z[Fim]
  B -->|Encontrou| C[Mover PDF para /boletos/processando]
  C --> D[Extrair dados do PDF]
  D --> E{Dados obrigatórios ok?}
  E -->|Não| E1[Registrar erro] --> E2[Mover para /boletos/erro] --> Z
  E -->|Sim| F[Resolver fornecedor (stakeholderId)]
  F --> G{Fornecedor encontrado?}
  G -->|Não| G1[Registrar erro/pendência] --> E2
  G -->|Sim| H[Montar payload]
  H --> I[Gerar idempotência]
  I --> J{Já foi processado?}
  J -->|Sim| J1[Registrar duplicidade] --> K[Mover para /boletos/processados] --> Z
  J -->|Não| L[POST pagamento no Nibo]
  L --> M{Resposta 2xx?}
  M -->|Não| M1[Registrar erro] --> E2
  M -->|Sim| N[Salvar evidência] --> K --> Z

