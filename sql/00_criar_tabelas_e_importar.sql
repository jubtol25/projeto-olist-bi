-- Cria as tabelas com os tipos de dado corretos e importa os CSVs tratados
-- direto via BULK INSERT (sem passar pelo assistente grafico, que tem bugs
-- de conversao de casas decimais). Rode este script inteiro de uma vez
-- no SSMS, com o banco "olist_bi" selecionado.

USE olist_bi;
GO

IF OBJECT_ID('dbo.fact_orders', 'U') IS NOT NULL DROP TABLE dbo.fact_orders;
IF OBJECT_ID('dbo.dim_products', 'U') IS NOT NULL DROP TABLE dbo.dim_products;
GO

CREATE TABLE dbo.fact_orders (
    order_id                       NVARCHAR(50)   NOT NULL,
    customer_id                    NVARCHAR(50)   NOT NULL,
    customer_state                 NVARCHAR(5)    NULL,
    customer_city                  NVARCHAR(100)  NULL,
    order_status                   NVARCHAR(30)   NULL,
    order_purchase_timestamp       DATETIME2      NULL,
    order_delivered_customer_date  DATETIME2      NULL,
    order_estimated_delivery_date  DATETIME2      NULL,
    delivery_delay_days            INT            NULL,
    is_late                        INT            NULL,
    purchase_month                 NVARCHAR(10)   NULL,
    purchase_weekday               NVARCHAR(15)   NULL,
    n_items                        INT            NULL,
    items_price                    DECIMAL(12,2)  NULL,
    freight_value                  DECIMAL(12,2)  NULL,
    avg_distance_km                FLOAT          NULL,
    main_category                  NVARCHAR(50)   NULL,
    seller_state                   NVARCHAR(5)    NULL,
    payment_value                  DECIMAL(12,2)  NULL,
    payment_installments_max       INT            NULL,
    payment_types                  NVARCHAR(200)  NULL,
    review_score                   INT            NULL
);
GO

CREATE TABLE dbo.dim_products (
    product_id                     NVARCHAR(50) NOT NULL,
    product_category_name          NVARCHAR(50) NULL,
    product_category_name_english  NVARCHAR(50) NULL
);
GO

BULK INSERT dbo.fact_orders
FROM 'C:\Users\julia\Downloads\projeto-olist-bi\data\processed\fact_orders.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    FIELDQUOTE = '"',
    CODEPAGE = '65001',
    TABLOCK
);
GO

BULK INSERT dbo.dim_products
FROM 'C:\Users\julia\Downloads\projeto-olist-bi\data\processed\dim_products.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    FIELDQUOTE = '"',
    CODEPAGE = '65001',
    TABLOCK
);
GO

-- Conferencia rapida: deve dar 99441 e 32951
SELECT COUNT(*) AS total_fact_orders FROM dbo.fact_orders;
SELECT COUNT(*) AS total_dim_products FROM dbo.dim_products;
GO
