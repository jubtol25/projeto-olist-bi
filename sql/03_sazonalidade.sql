-- Pergunta 3: como vendas e ticket medio variam por mes e por dia da semana?
SELECT
    purchase_month,
    COUNT(*)                        AS n_pedidos,
    ROUND(SUM(items_price), 2)      AS receita,
    ROUND(AVG(items_price), 2)      AS ticket_medio
FROM fact_orders
GROUP BY purchase_month
ORDER BY purchase_month;

-- por dia da semana
SELECT
    purchase_weekday,
    COUNT(*)                     AS n_pedidos,
    ROUND(AVG(items_price), 2)   AS ticket_medio
FROM fact_orders
GROUP BY purchase_weekday
ORDER BY n_pedidos DESC;
