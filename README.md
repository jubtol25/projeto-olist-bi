# Análise de Vendas e Logística — E-commerce Olist

Projeto de Business Intelligence construído a partir do [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), com o objetivo de investigar padrões de vendas, atrasos de entrega e satisfação do cliente em um marketplace brasileiro, e transformar esses achados em um dashboard interativo.

## Contexto

A Olist é uma plataforma que conecta pequenos e médios lojistas brasileiros aos principais marketplaces do país. O dataset público reúne cerca de 100 mil pedidos feitos entre 2016 e 2018, com informações de pedido, pagamento, frete, avaliação do cliente, vendedor e localização geográfica.

Este projeto simula o trabalho de um(a) analista de BI que precisa entender **onde a operação está perdendo eficiência e satisfação do cliente**, e comunicar isso para áreas de negócio através de um dashboard.

## Perguntas de negócio

O projeto foi guiado pelas seguintes perguntas:

1. **Atraso de entrega**: qual o percentual de pedidos entregues após o prazo estimado, e como isso varia por região (estado) e por categoria de produto?
2. **Satisfação do cliente**: existe relação entre atraso na entrega e a nota de avaliação (review score) dada pelo cliente?
3. **Sazonalidade**: como o volume de vendas e o ticket médio variam ao longo dos meses/dias da semana? Existem picos que a operação deveria se preparar melhor para atender?
4. **Categorias e regiões mais relevantes**: quais categorias de produto e quais estados geram mais receita, e quais têm a pior relação entre receita e satisfação/atraso?
5. **Frete**: qual a relação entre o valor do frete e a distância entre vendedor e cliente, e isso impacta a decisão de compra (cancelamentos)?

> Ajuste esta lista conforme os achados forem aparecendo — no BI é normal a análise revelar novas perguntas pelo caminho.

## Fonte de dados

- **Dataset**: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle, dados públicos, licença CC BY-NC-SA 4.0)
- Baixe os arquivos `.csv` e coloque em `data/raw/` (essa pasta é ignorada pelo git — veja `.gitignore`)

## Ferramentas utilizadas

- **SQL** — modelagem e consultas (ex.: SQLite/PostgreSQL local)
- **Python** (pandas) — limpeza, tratamento e enriquecimento dos dados
- **Power BI** — modelagem semântica (DAX) e dashboard final

## Estrutura do repositório

```
projeto-olist-bi/
├── data/
│   ├── raw/            # dados originais baixados do Kaggle (não versionados)
│   └── processed/      # dados já tratados, prontos para o Power BI
├── sql/                # scripts de criação de tabelas e queries de análise
├── notebooks/          # notebooks/scripts Python de limpeza e exploração
├── dashboard/          # arquivo .pbix e/ou exports (PDF, imagens) do dashboard
├── docs/               # prints e material de apoio para o README
└── README.md
```

## Como reproduzir

1. Baixe o dataset no Kaggle e extraia os `.csv` para `data/raw/`.
2. Rode os scripts em `notebooks/` para limpar e tratar os dados (gera arquivos em `data/processed/`).
3. Use os scripts em `sql/` para criar as tabelas e rodar as queries de análise (em SQLite, PostgreSQL, ou direto no Power Query).
4. Abra `dashboard/projeto-olist.pbix` no Power BI Desktop, aponte a fonte de dados para `data/processed/` e atualize o modelo.

## Principais insights

_(preencher depois de concluir a análise — resuma aqui em 3 a 5 bullets os achados mais relevantes, com números. É a parte que mais chama atenção de quem visita o repositório.)_

## Dashboard

_(inserir aqui 1-2 prints do dashboard final, salvos em `docs/`, por exemplo:)_

```
![Visão geral do dashboard](docs/dashboard-overview.png)
```

## Autora

Juliane Tolino — Analista de Business Intelligence
[LinkedIn](#) · [GitHub](#)
