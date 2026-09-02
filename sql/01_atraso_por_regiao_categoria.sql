-- Pergunta 1: qual o % de atraso na entrega por estado e categoria de produto?
-- (SQL Server / T-SQL)
SELECT TOP 20
    customer_state,
    main_category,
    COUNT(*)                                                     AS total_pedidos,
    SUM(CAST(is_late AS INT))                                    AS pedidos_atrasados,
    ROUND(100.0 * SUM(CAST(is_late AS INT)) / COUNT(*), 1)        AS pct_atraso
FROM fact_orders
WHERE order_delivered_customer_date IS NOT NULL
GROUP BY customer_state, main_category
HAVING COUNT(*) >= 20
ORDER BY pct_atraso DESC;
