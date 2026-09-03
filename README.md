# Análise de Vendas e Logística — E-commerce Olist

Projeto de Business Intelligence construído a partir do [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), com o objetivo de investigar padrões de vendas, atrasos de entrega e satisfação do cliente em um marketplace brasileiro, e transformar esses achados em um dashboard interativo.

## Contexto

A Olist é uma plataforma que conecta pequenos e médios lojistas brasileiros aos principais marketplaces do país. O dataset público reúne cerca de 100 mil pedidos feitos entre 2016 e 2018, com informações de pedido, pagamento, frete, avaliação do cliente, vendedor e localização geográfica.

Este projeto simula o trabalho de um(a) analista de BI que precisa entender **onde a operação está perdendo eficiência e satisfação do cliente**, e comunicar isso para áreas de negócio através de um dashboard.

## Perguntas de negócio

O projeto foi guiado pelas 5 perguntas abaixo — cada uma respondida com base nas queries em `sql/01` a `sql/05` e no dashboard final.

**1. Atraso de entrega — qual o percentual de pedidos entregues após o prazo estimado, e como isso varia por região e categoria?**

> **Resposta:** No geral, **6,77%** dos pedidos entregues chegam depois da data estimada. Esse percentual não é uniforme: por estado, varia de ~21,4% em Alagoas (o pior caso) até ~9,7% em Mato Grosso do Sul (um dos melhores). Olhando por combinação estado+categoria, o pior caso chega a **45,5%** (Maranhão, categoria housewares). O padrão geral é claro: estados do Norte/Nordeste, mais distantes dos centros de distribuição concentrados no Sudeste, têm taxas de atraso bem mais altas.

**2. Satisfação do cliente — existe relação entre atraso e nota de avaliação?**

> **Resposta:** Sim, e é a relação mais forte encontrada no projeto: pedidos entregues **com atraso** têm nota média de **2,27** (de 5), contra **4,29** para os entregues **no prazo**. O atraso na entrega é, disparado, o fator que mais derruba a satisfação do cliente nesse marketplace.

**3. Sazonalidade — como vendas e ticket médio variam ao longo do tempo?**

> **Resposta:** O volume de pedidos cresce de forma consistente entre set/2016 e meados de 2018 (com uma queda no fim que é uma limitação do dataset, não do negócio — ver nota na seção Dashboard). Por dia da semana, segunda-feira concentra o maior volume de pedidos (16,2 mil) e vai caindo ao longo da semana até sábado, o mais fraco (10,9 mil) — um padrão típico de e-commerce, com mais compras em dias úteis.

**4. Categorias e regiões mais relevantes — quais geram mais receita, e quais têm pior relação receita x satisfação/atraso?**

> **Resposta:** As categorias que mais geram receita são **saúde/beleza** (R$ 1,26 Mi), **relógios/presentes** (R$ 1,20 Mi) e **cama/mesa/banho** (R$ 1,04 Mi). Cruzando com atraso: combinações de alto volume mas atraso elevado (como saúde/beleza no Maranhão, com 24,4% de atraso) representam o maior risco — são categorias relevantes financeiramente, mas com experiência de entrega ruim numa região específica, o que pede atenção prioritária da operação.

**5. Frete — qual a relação entre frete, distância e cancelamento?**

> **Resposta:** O frete médio sobe de forma esperada com a distância entre vendedor e cliente: de **R$ 14,63** (até 200km) para **R$ 35,53** (acima de 1.000km). O achado contraintuitivo é que a taxa de cancelamento faz o caminho **inverso**, caindo de **1,35%** (até 200km) para **0,26%** (acima de 1.000km) — ou seja, pedidos de longa distância cancelam menos, não mais, apesar do frete mais caro. Uma hipótese é que compras de longa distância tendem a ser mais deliberadas (o cliente já sabe que vai pagar mais caro e decide mesmo assim), enquanto compras locais têm mais desistência por impulso.

> As perguntas originais que guiaram o projeto estão preservadas acima; no dia a dia de BI é normal que a análise revele novas perguntas pelo caminho — os achados extras (como a hipótese do item 5) valem como próximos passos de investigação.

## Fonte de dados

- **Dataset**: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle, dados públicos, licença CC BY-NC-SA 4.0)
- Baixe os arquivos `.csv` e coloque em `data/raw/` (essa pasta é ignorada pelo git — veja `.gitignore`)

## Ferramentas utilizadas

- **SQL Server** (T-SQL) — modelagem e consultas, via SQL Server Express + SSMS
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
2. Rode `python notebooks/clean_and_load.py` para limpar e tratar os dados (gera `data/processed/fact_orders.csv` e `data/processed/dim_products.csv`).
3. No SQL Server Management Studio (SSMS), crie um banco chamado `olist_bi` e rode o script `sql/00_criar_tabelas_e_importar.sql` (cria as tabelas com os tipos corretos e importa os CSVs via `BULK INSERT` — mais confiável do que o assistente gráfico de importação, que tem bugs de conversão decimal).
4. Rode as queries em `sql/01` a `sql/05` (T-SQL) direto no SSMS para explorar as respostas às perguntas de negócio.
5. Abra `dashboard/Projeto Olist.pbix` no Power BI Desktop, conecte na fonte SQL Server (`localhost\SQLEXPRESS`, banco `olist_bi`) e atualize o modelo.

## Evidências (queries)

Prints das queries em `sql/` rodadas no SSMS, mostrando os números por trás das respostas acima:

![Query 01: atraso por estado e categoria](docs/query-01-atraso-regiao-categoria.png)

![Query 02: atraso vs nota de avaliação](docs/query-02-atraso-vs-avaliacao.png)

## Dashboard

O dashboard final tem 2 páginas no Power BI (`dashboard/Projeto Olist.pbix`):

**Visão Geral** — KPIs principais, receita por categoria, % de atraso por estado e evolução mensal de pedidos.

![Dashboard - Visão Geral](docs/dashboard-pagina1-visao-geral.png)

**Logística e Frete** — frete médio e % de cancelamento por faixa de distância (mostrando o achado contraintuitivo: frete sobe, cancelamento cai), e pedidos por dia da semana.

![Dashboard - Logística e Frete](docs/dashboard-pagina2-logistica-frete.png)

> Nota: a queda brusca de pedidos em set/out de 2018 no gráfico de evolução mensal não reflete uma queda real de vendas — é uma limitação conhecida do dataset público da Olist, cuja coleta de dados é bem esparsa a partir de agosto/2018.

## Autora

Juliane Tolino — Analista de Business Intelligence
[LinkedIn](#) · [GitHub](#)
