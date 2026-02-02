flowchart TD
  A[Início: PDF chega na pasta /boletos/entrada] --> B{Detectar PDFs novos}
  B -->|Nenhum| Z[Fim]
  B -->|Encontrou| C[Mover PDF para /boletos/processando]

  C --> D[Extrair dados do PDF\n(valor, vencimento, fornecedor, descricao...)]
  D --> E{Dados obrigatórios ok?}

  E -->|Não| E1[Registrar erro\n+ salvar motivo] --> E2[Mover PDF para /boletos/erro] --> Z
  E -->|Sim| F[Resolver fornecedor no Nibo\n(stakeholderId)]

  F --> G{Fornecedor encontrado?}
  G -->|Não| G1[Registrar erro / pendência\nFornecedor não cadastrado] --> E2
  G -->|Sim| H[Montar payload do pagamento]

  H --> I[Gerar chave de idempotência\n(hash/linha digitável/cnpj+venc+valor)]
  I --> J{Já foi processado?}

  J -->|Sim| J1[Registrar duplicidade\npular envio] --> K[Mover PDF para /boletos/processados] --> Z
  J -->|Não| L[POST pagamento na API do Nibo]

  L --> M{Resposta 2xx?}
  M -->|Não| M1[Registrar erro\nresponse body + status] --> E2
  M -->|Sim| N[Salvar evidência\n(ID do Nibo / resposta)] --> K[Mover PDF para /boletos/processados] --> Z
